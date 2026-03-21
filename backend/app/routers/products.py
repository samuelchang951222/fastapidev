from __future__ import annotations

from typing import List, Optional

from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy import desc, or_
from sqlalchemy.orm import Session

from ..db import get_db
from ..models import Category as CategoryModel
from ..models import Product as ProductModel
from ..schemas import Product

router = APIRouter(prefix="/api", tags=["products"])


@router.get("/products", response_model=List[Product])
def list_products(
    category: Optional[str] = Query(default=None),
    q: Optional[str] = Query(default=None),
    sort: str = Query(default="featured"),
    db: Session = Depends(get_db),
) -> List[Product]:
    query = db.query(ProductModel, CategoryModel).join(
        CategoryModel, ProductModel.category_slug == CategoryModel.slug
    )

    if category and category != "all":
        query = query.filter(ProductModel.category_slug == category)

    if q:
        needle = f"%{q.strip()}%"
        query = query.filter(
            or_(
                ProductModel.name.like(needle),
                ProductModel.description.like(needle),
                CategoryModel.name.like(needle),
            )
        )

    if sort == "priceAsc":
        query = query.order_by(ProductModel.price.asc())
    elif sort == "priceDesc":
        query = query.order_by(ProductModel.price.desc())
    elif sort == "newest":
        query = query.order_by(desc(ProductModel.created_at))
    else:
        query = query.order_by(desc(ProductModel.featured_rank))

    rows = query.all()
    return [
        Product(
            id=p.id,
            name=p.name,
            categorySlug=p.category_slug,
            categoryName=c.name,
            description=p.description,
            price=p.price,
            compareAtPrice=p.compare_at_price,
            badge=p.badge,
            imageUrl=p.image_url,
            stock=p.stock,
            unit=p.unit,
            createdAt=p.created_at,
            featuredRank=p.featured_rank,
            isWeeklyPick=p.is_weekly_pick,
        )
        for (p, c) in rows
    ]


@router.get("/products/{product_id}", response_model=Product)
def get_product(product_id: int, db: Session = Depends(get_db)) -> Product:
    row = (
        db.query(ProductModel, CategoryModel)
        .join(CategoryModel, ProductModel.category_slug == CategoryModel.slug)
        .filter(ProductModel.id == product_id)
        .first()
    )
    if not row:
        raise HTTPException(status_code=404, detail="Product not found")
    p, c = row
    return Product(
        id=p.id,
        name=p.name,
        categorySlug=p.category_slug,
        categoryName=c.name,
        description=p.description,
        price=p.price,
        compareAtPrice=p.compare_at_price,
        badge=p.badge,
        imageUrl=p.image_url,
        stock=p.stock,
        unit=p.unit,
        createdAt=p.created_at,
        featuredRank=p.featured_rank,
        isWeeklyPick=p.is_weekly_pick,
    )

