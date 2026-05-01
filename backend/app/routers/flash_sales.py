"""
限時特賣路由
"""
from __future__ import annotations
from typing import List
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from ..db import get_db
from ..models import FlashSale as FlashSaleModel
from ..schemas import FlashSaleItem

router = APIRouter(prefix="/api", tags=["flash-sales"])


@router.get("/flash-sales", response_model=List[FlashSaleItem])
def get_flash_sales(db: Session = Depends(get_db)) -> List[FlashSaleItem]:
    rows = db.query(FlashSaleModel).order_by(FlashSaleModel.id.asc()).all()
    return [FlashSaleItem(productId=r.product_id, label=r.label) for r in rows]

