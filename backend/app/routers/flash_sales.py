from __future__ import annotations

from typing import List

from fastapi import APIRouter

from ..data.seed import FLASH_SALES
from ..schemas import FlashSaleItem

router = APIRouter(prefix="/api", tags=["flash-sales"])


@router.get("/flash-sales", response_model=List[FlashSaleItem])
def get_flash_sales() -> List[FlashSaleItem]:
    return [FlashSaleItem(**x) for x in FLASH_SALES]

