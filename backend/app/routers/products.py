from __future__ import annotations

from typing import List, Optional

from fastapi import APIRouter, HTTPException, Query

from ..data.seed import PRODUCTS
from ..schemas import Product

router = APIRouter(prefix="/api", tags=["products"])


def _matches_q(p: dict, q: str) -> bool:
    if not q:
        return True
    needle = q.strip().lower()
    hay = f"{p.get('name','')} {p.get('description','')} {p.get('categoryName','')}".lower()
    return needle in hay


def _sort(products: list[dict], sort: str) -> list[dict]:
    if sort == "priceAsc":
        return sorted(products, key=lambda x: int(x.get("price") or 0))
    if sort == "priceDesc":
        return sorted(products, key=lambda x: int(x.get("price") or 0), reverse=True)
    if sort == "newest":
        return sorted(products, key=lambda x: int(x.get("createdAt") or 0), reverse=True)
    return sorted(products, key=lambda x: int(x.get("featuredRank") or 0), reverse=True)


@router.get("/products", response_model=List[Product])
def list_products(
    category: Optional[str] = Query(default=None),
    q: Optional[str] = Query(default=None),
    sort: str = Query(default="featured"),
) -> List[Product]:
    items = PRODUCTS
    if category and category != "all":
        items = [p for p in items if p.get("categorySlug") == category]
    if q:
        items = [p for p in items if _matches_q(p, q)]
    items = _sort(items, sort)
    return [Product(**p) for p in items]


@router.get("/products/{product_id}", response_model=Product)
def get_product(product_id: int) -> Product:
    for p in PRODUCTS:
        if int(p.get("id")) == product_id:
            return Product(**p)
    raise HTTPException(status_code=404, detail="Product not found")

