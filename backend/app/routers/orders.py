from __future__ import annotations

import time
from typing import List

from fastapi import APIRouter
from supabase import create_client

from ..schemas import CreateOrderRequest, Order
from ..supabase_config import SUPABASE_KEY, SUPABASE_URL

router = APIRouter(prefix="/api", tags=["orders"])

_supabase = create_client(SUPABASE_URL, SUPABASE_KEY)


@router.post("/orders", response_model=Order)
def create_order(req: CreateOrderRequest) -> Order:
    now = int(time.time())

    # 1. 插入 orders 主表
    order_data = {
        "user_id": 0,
        "recipient_name": req.name,
        "phone": req.phone,
        "address": req.address,
        "total_price": req.total,
        "created_at": now,
        "payment_status": "pending",
        "trade_no": "",
        "payment_method": "",
        "address1": "",
        "address2": "",
    }
    result = _supabase.table("orders").insert(order_data).execute()

    if not result.data:
        raise RuntimeError("訂單寫入失敗")

    order_row = result.data[0]
    order_id = order_row["id"]

    # 2. 插入 order_items 明細
    items_data = [
        {
            "order_id": order_id,
            "product_id": it.productId,
            "product_name": it.productName,
            "unit_price": it.price,
            "quantity": it.quantity,
            "subtotal": it.price * it.quantity,
        }
        for it in req.items
    ]
    _supabase.table("order_items").insert(items_data).execute()

    # 3. 回傳完整訂單
    return Order(
        id=order_id,
        name=req.name,
        phone=req.phone,
        address=req.address,
        items=req.items,
        total=req.total,
        status="pending",
        createdAt=now,
    )


@router.get("/orders", response_model=List[Order])
def list_orders() -> List[Order]:
    result = _supabase.table("orders").select("*").order("created_at", desc=True).execute()
    return [
        Order(
            id=r["id"],
            name=r.get("recipient_name", ""),
            phone=r.get("phone", ""),
            address=r.get("address", ""),
            items=[],
            total=r.get("total_price", 0),
            status=r.get("payment_status", "pending"),
            createdAt=r.get("created_at", 0),
        )
        for r in (result.data or [])
    ]
