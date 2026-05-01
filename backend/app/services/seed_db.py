"""
資料庫初始化
"""
from __future__ import annotations
from sqlalchemy.orm import Session
from ..data.seed import CATEGORIES, FLASH_SALES, PRODUCTS
from ..models import Category, FlashSale, Product


def seed_if_empty(db: Session) -> None:
    has_any = db.query(Category).limit(1).first()
    if has_any:
        return

    for c in CATEGORIES:
        db.add(Category(id=c["id"], name=c["name"], slug=c["slug"]))
    db.flush()

    for p in PRODUCTS:
        db.add(
            Product(
                id=p["id"],
                name=p["name"],
                category_slug=p["categorySlug"],
                description=p["description"],
                price=int(p["price"]),
                compare_at_price=p.get("compareAtPrice"),
                badge=p.get("badge"),
                image_url=p.get("imageUrl"),
                stock=int(p.get("stock") or 0),
                unit=p.get("unit") or "份",
                created_at=int(p.get("createdAt") or 0),
                featured_rank=int(p.get("featuredRank") or 0),
                is_weekly_pick=bool(p.get("isWeeklyPick") or False),
            )
        )
    db.flush()

    for fs in FLASH_SALES:
        db.add(FlashSale(product_id=int(fs["productId"]), label=fs.get("label")))

    db.commit()

