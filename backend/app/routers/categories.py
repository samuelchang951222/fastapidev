from __future__ import annotations

from typing import List

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from ..db import get_db
from ..models import Category as CategoryModel
from ..schemas import Category

router = APIRouter(prefix="/api", tags=["categories"])


@router.get("/categories", response_model=List[Category])
def get_categories(db: Session = Depends(get_db)) -> List[Category]:
    items = db.query(CategoryModel).order_by(CategoryModel.id.asc()).all()
    return [Category(id=c.id, name=c.name, slug=c.slug) for c in items]

