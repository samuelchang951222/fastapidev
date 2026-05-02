from __future__ import annotations

import hashlib
import json
import secrets
import time
from typing import Optional

import bcrypt
from fastapi import APIRouter, HTTPException, Header
from pydantic import BaseModel
from supabase import create_client

from ..supabase_config import SUPABASE_KEY, SUPABASE_URL

router = APIRouter(prefix="/api/auth", tags=["auth"])

_supabase = create_client(SUPABASE_URL, SUPABASE_KEY)

# 記憶體 token 儲存: token -> user_id
_token_store: dict[str, int] = {}
_token_expiry: dict[str, int] = {}


# ── Schema ──

class RegisterRequest(BaseModel):
    email: str
    name: str
    password: str
    phone: str = ""
    address: str = ""


class LoginRequest(BaseModel):
    email: str
    password: str


class UpdateProfileRequest(BaseModel):
    name: Optional[str] = None
    phone: Optional[str] = None
    address: Optional[str] = None


class AuthResponse(BaseModel):
    token: str
    user: dict


# ── Helper ──

def _format_user(user: dict) -> dict:
    return {
        "id": user["id"],
        "email": user.get("email", ""),
        "name": user.get("name", ""),
        "phone": user.get("phone", "") or "",
        "address": user.get("address", "") or "",
    }


def _get_user_from_token(token: str) -> int | None:
    user_id = _token_store.get(token)
    if user_id is None:
        return None
    exp = _token_expiry.get(token, 0)
    if time.time() > exp:
        _token_store.pop(token, None)
        _token_expiry.pop(token, None)
        return None
    return user_id


# ── Endpoints ──

@router.post("/register")
def register(req: RegisterRequest) -> AuthResponse:
    existing = _supabase.table("users").select("id").eq("email", req.email).execute()
    if existing.data:
        raise HTTPException(status_code=400, detail="此 Email 已被註冊")

    hashed = bcrypt.hashpw(req.password.encode(), bcrypt.gensalt()).decode()

    result = _supabase.table("users").insert({
        "email": req.email,
        "name": req.name,
        "hashed_password": hashed,
        "phone": req.phone,
        "address": req.address,
    }).execute()

    if not result.data:
        raise HTTPException(status_code=500, detail="註冊失敗")

    user = result.data[0]
    token = _create_token(user["id"])
    return AuthResponse(token=token, user=_format_user(user))


@router.post("/login")
def login(req: LoginRequest) -> AuthResponse:
    result = _supabase.table("users").select("*").eq("email", req.email).execute()
    if not result.data:
        raise HTTPException(status_code=401, detail="Email 或密碼錯誤")

    user = result.data[0]
    stored = user.get("hashed_password", "")

    if stored.startswith("$2"):
        valid = bcrypt.checkpw(req.password.encode(), stored.encode())
    else:
        valid = _verify_pbkdf2(req.password, stored)

    if not valid:
        raise HTTPException(status_code=401, detail="Email 或密碼錯誤")

    token = _create_token(user["id"])
    return AuthResponse(token=token, user=_format_user(user))


@router.get("/me")
def get_me(authorization: str | None = Header(default=None)) -> dict:
    if not authorization or not authorization.startswith("Bearer "):
        raise HTTPException(status_code=401, detail="未登入")
    token = authorization[7:]
    user_id = _get_user_from_token(token)
    if user_id is None:
        raise HTTPException(status_code=401, detail="Token 已過期或無效")

    result = _supabase.table("users").select("*").eq("id", user_id).execute()
    if not result.data:
        raise HTTPException(status_code=401, detail="使用者不存在")
    return {"user": _format_user(result.data[0])}


@router.put("/profile")
def update_profile(req: UpdateProfileRequest,
                   authorization: str | None = Header(default=None)) -> dict:
    if not authorization or not authorization.startswith("Bearer "):
        raise HTTPException(status_code=401, detail="未登入")
    token = authorization[7:]
    user_id = _get_user_from_token(token)
    if user_id is None:
        raise HTTPException(status_code=401, detail="Token 已過期或無效")

    # 只更新有提供的欄位
    updates = {}
    if req.name is not None:
        updates["name"] = req.name
    if req.phone is not None:
        updates["phone"] = req.phone
    if req.address is not None:
        updates["address"] = req.address

    if updates:
        _supabase.table("users").update(updates).eq("id", user_id).execute()

    result = _supabase.table("users").select("*").eq("id", user_id).execute()
    return {"user": _format_user(result.data[0])}


@router.post("/logout")
def logout(authorization: str | None = Header(default=None)) -> dict:
    if authorization and authorization.startswith("Bearer "):
        token = authorization[7:]
        _token_store.pop(token, None)
        _token_expiry.pop(token, None)
    return {"ok": True}


# ── 購物車同步 ──

@router.get("/cart")
def get_cart(authorization: str | None = Header(default=None)) -> dict:
    if not authorization or not authorization.startswith("Bearer "):
        raise HTTPException(status_code=401, detail="未登入")
    token = authorization[7:]
    user_id = _get_user_from_token(token)
    if user_id is None:
        raise HTTPException(status_code=401, detail="Token 已過期或無效")

    result = _supabase.table("users").select("cart_data").eq("id", user_id).execute()
    if not result.data:
        return {"items": {}}
    raw = result.data[0].get("cart_data", "[]")
    try:
        items = json.loads(raw)
    except Exception:
        items = []
    return {"items": items}


@router.put("/cart")
def save_cart(body: dict, authorization: str | None = Header(default=None)) -> dict:
    if not authorization or not authorization.startswith("Bearer "):
        raise HTTPException(status_code=401, detail="未登入")
    token = authorization[7:]
    user_id = _get_user_from_token(token)
    if user_id is None:
        raise HTTPException(status_code=401, detail="Token 已過期或無效")

    items = body.get("items", {})
    _supabase.table("users").update({"cart_data": json.dumps(items)}).eq("id", user_id).execute()
    return {"ok": True}


# ── Internal ──

def _create_token(user_id: int) -> str:
    token = secrets.token_hex(32)
    _token_store[token] = user_id
    _token_expiry[token] = int(time.time()) + 86400 * 7
    return token


def _verify_pbkdf2(password: str, stored: str) -> bool:
    """驗證 $pbkdf2-sha256$rounds$salt$hash 格式"""
    try:
        parts = stored.split("$")
        if len(parts) < 5:
            if len(parts) >= 4:
                rounds = int(parts[2])
                salt = parts[3]
                hash_hex = parts[4] if len(parts) > 4 else ""
            else:
                return False
        else:
            rounds = int(parts[2])
            salt = parts[3]
            hash_hex = parts[4] if len(parts) > 4 else ""

        derived = hashlib.pbkdf2_hmac("sha256", password.encode(), salt.encode(), rounds)
        return derived.hex() == hash_hex
    except Exception:
        return False
