from __future__ import annotations

import time
from typing import List

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from ..auth import get_current_user
from ..db import get_db
from ..models import Order as OrderModel
from ..models import OrderItem as OrderItemModel
from ..models import Product as ProductModel
from ..schemas import OrderCreate, OrderItemOut, OrderOut, UserOut

router = APIRouter(prefix="/api/orders", tags=["orders"])


@router.post("", response_model=OrderOut, status_code=status.HTTP_201_CREATED)
def create_order(
    payload: OrderCreate,
    db: Session = Depends(get_db),
    current_user: UserOut = Depends(get_current_user),
) -> OrderOut:
    if not payload.items:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="購物車是空的")

    product_ids = {item.productId for item in payload.items}
    products = db.query(ProductModel).filter(ProductModel.id.in_(product_ids)).all()
    found_by_id = {p.id: p for p in products}

    order = OrderModel(
        user_id=current_user.id,
        recipient_name=payload.recipientName,
        phone=payload.phone,
        address=payload.address,
        total_price=0,
        created_at=int(time.time()),
    )
    db.add(order)
    db.flush()

    total = 0
    items_out: List[OrderItemOut] = []

    for item in payload.items:
        p = found_by_id.get(item.productId)
        if not p:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=f"商品不存在: {item.productId}")
        unit_price = int(p.price)
        quantity = max(1, int(item.quantity))
        subtotal = unit_price * quantity
        total += subtotal

        row = OrderItemModel(
            order_id=order.id,
            product_id=p.id,
            product_name=p.name,
            unit_price=unit_price,
            quantity=quantity,
            subtotal=subtotal,
        )
        db.add(row)

        items_out.append(
            OrderItemOut(
                productId=p.id,
                productName=p.name,
                unitPrice=unit_price,
                quantity=quantity,
                subtotal=subtotal,
            )
        )

    order.total_price = total
    db.commit()
    db.refresh(order)

    return OrderOut(
        id=order.id,
        totalPrice=order.total_price,
        createdAt=order.created_at,
        recipientName=order.recipient_name,
        phone=order.phone,
        address=order.address,
        items=items_out,
    )


@router.get("", response_model=List[OrderOut])
def list_my_orders(
    db: Session = Depends(get_db),
    current_user: UserOut = Depends(get_current_user),
) -> List[OrderOut]:
    orders = (
        db.query(OrderModel)
        .filter(OrderModel.user_id == current_user.id)
        .order_by(OrderModel.created_at.desc())
        .all()
    )

    results: List[OrderOut] = []
    for order in orders:
        items_out: List[OrderItemOut] = []
        for row in order.items:
            items_out.append(
                OrderItemOut(
                    productId=row.product_id,
                    productName=row.product_name,
                    unitPrice=row.unit_price,
                    quantity=row.quantity,
                    subtotal=row.subtotal,
                )
            )
        results.append(
            OrderOut(
                id=order.id,
                totalPrice=order.total_price,
                createdAt=order.created_at,
                recipientName=order.recipient_name,
                phone=order.phone,
                address=order.address,
                items=items_out,
            )
        )

    return results

