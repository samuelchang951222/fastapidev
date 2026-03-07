from __future__ import annotations

from typing import List

from fastapi import APIRouter

from ..data.seed import CATEGORIES
from ..schemas import Category

router = APIRouter(prefix="/api", tags=["categories"])


@router.get("/categories", response_model=List[Category])
def get_categories() -> List[Category]:
    return [Category(**c) for c in CATEGORIES]

