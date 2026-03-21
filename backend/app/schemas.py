from __future__ import annotations

from typing import List, Optional

from pydantic import BaseModel, Field, EmailStr


class Category(BaseModel):
    id: int
    name: str
    slug: str


class Product(BaseModel):
    id: int
    name: str
    categorySlug: str
    categoryName: str
    description: str
    price: int
    compareAtPrice: Optional[int] = None
    badge: Optional[str] = None
    imageUrl: Optional[str] = None
    stock: int = 0
    unit: str = "份"
    createdAt: int = Field(default=0, description="Unix epoch seconds (UI sorting only)")
    featuredRank: int = 0
    isWeeklyPick: bool = False


class FlashSaleItem(BaseModel):
    productId: int
    label: Optional[str] = None


class UserBase(BaseModel):
    email: EmailStr
    name: str


class UserCreate(UserBase):
    password: str


class UserOut(UserBase):
    id: int


class Token(BaseModel):
    access_token: str
    token_type: str = "bearer"


class TokenPayload(BaseModel):
    sub: str
    exp: int


class OrderItemCreate(BaseModel):
    productId: int
    quantity: int


class OrderCreate(BaseModel):
    recipientName: str
    phone: str
    address: str
    items: List[OrderItemCreate]


class OrderItemOut(BaseModel):
    productId: int
    productName: str
    unitPrice: int
    quantity: int
    subtotal: int


class OrderOut(BaseModel):
    id: int
    totalPrice: int
    createdAt: int
    recipientName: str
    phone: str
    address: str
    items: List[OrderItemOut]


