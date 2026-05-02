from __future__ import annotations

from typing import Optional

from pydantic import BaseModel, Field


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


class OrderItem(BaseModel):
    productId: int
    productName: str
    price: int
    quantity: int


class CreateOrderRequest(BaseModel):
    name: str
    phone: str
    address: str
    items: list[OrderItem]
    total: int


class Order(BaseModel):
    id: int
    name: str
    phone: str
    address: str
    items: list[OrderItem]
    total: int
    status: str = "pending"
    createdAt: int

