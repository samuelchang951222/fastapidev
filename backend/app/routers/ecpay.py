"""
綠界支付路由
"""
import hashlib
import urllib.parse
import time
import uuid
from datetime import datetime
from fastapi import APIRouter, Request, HTTPException, Depends
from fastapi.responses import PlainTextResponse, HTMLResponse
from sqlalchemy.orm import Session
from app import models, schemas
from app.auth import get_current_user
from app.db import get_db

router = APIRouter(prefix="/api/ecpay", tags=["ECPay"])

HASH_KEY = "5294y06JbISpM5x9"
HASH_IV = "v77hoKGq4kWxNNIS"
MERCHANT_ID = "2000132"


def calculate_check_mac_value(data: dict) -> str:
    filtered_data = {k: v for k, v in data.items() if k != "CheckMacValue"}
    sorted_keys = sorted(filtered_data.keys())
    query_str = "&".join([f"{k}={filtered_data[k]}" for k in sorted_keys])
    raw_str = f"HashKey={HASH_KEY}&{query_str}&HashIV={HASH_IV}"
    url_encoded = urllib.parse.quote_plus(raw_str).replace("%20", "+")
    url_encoded = url_encoded.replace("%2D", "-").replace("%5F", "_").replace("%2E", ".").replace("%21", "!")
    return hashlib.sha256(url_encoded.lower().encode("utf-8")).hexdigest().upper()


@router.post("/checkout")
async def ecpay_checkout(order_data: schemas.OrderCreate, current_user: schemas.UserOut = Depends(get_current_user), db: Session = Depends(get_db)):
    trade_no = f"OD{datetime.now().strftime('%Y%m%d%H%M%S')}{uuid.uuid4().hex[:4].upper()}"
    trade_date = datetime.now().strftime("%Y/%m/%d %H:%M:%S")
    total_price = 0
    order_items = []

    try:
        for item in order_data.items:
            product = db.query(models.Product).filter(models.Product.id == item.productId).first()
            if not product:
                raise HTTPException(status_code=404, detail=f"找不到商品 ID: {item.productId}")
            if product.stock < item.quantity:
                raise HTTPException(status_code=400, detail=f"商品 {product.name} 庫存不足")
            
            total_price += product.price * item.quantity
            order_items.append(models.OrderItem(
                product_id=product.id,
                product_name=product.name,
                unit_price=product.price,
                quantity=item.quantity
            ))

        order = models.Order(
            user_id=current_user.id,
            recipient_name=order_data.recipientName,
            phone=order_data.phone,
            address1=order_data.address1,
            address2=order_data.address2,
            total_price=total_price,
            created_at=int(time.time()),
            payment_status="UNPAID",
            trade_no=trade_no,
            payment_method="ecpay"
        )
        db.add(order)
        db.flush()

        for order_item in order_items:
            order_item.order_id = order.id
            db.add(order_item)

        db.commit() # 一切無誤，將主檔與明細一併永久寫入

    except HTTPException:
        db.rollback() # 若發生預期內的錯誤（如庫存不足），復原所有資料庫操作
        raise
    except Exception as e:
        print(f"Error in checkout: {e}")
        db.rollback() # 若發生未預期錯誤，復原操作避免產生髒資料
        raise HTTPException(status_code=500, detail="訂單建立失敗")

    ecpay_params = {
        "MerchantID": MERCHANT_ID,
        "MerchantTradeNo": order.trade_no,
        "MerchantTradeDate": trade_date,
        "PaymentType": "aio",
        "TotalAmount": str(total_price),
        "TradeDesc": "商城購物",
        "ItemName": "商城商品一批", # 統一品名，避免特殊字元或超長字元導致綠界 API 崩潰
        "ReturnURL": "https://你的網址/api/ecpay/return",
        "ClientBackURL": "https://你的網址/payment-success",
        "ChoosePayment": "Credit",
        "EncryptType": "1",
    }

    # 統一呼叫加密函式
    ecpay_params["CheckMacValue"] = calculate_check_mac_value(ecpay_params)

    # 生成 HTML (使用更簡潔安全的字串推導式)
    inputs = "".join(f'<input type="hidden" name="{k}" value="{v}">' for k, v in ecpay_params.items())
    html_form = f"""
    <!DOCTYPE html><html><head><title>跳轉中...</title></head><body>
        <form id="ecpay-form" method="POST" action="https://payment-stage.ecpay.com.tw/Cashier/AioCheckOut/V5">
            {inputs}
        </form>
        <script>document.getElementById('ecpay-form').submit();</script>
    </body></html>
    """
    return HTMLResponse(content=html_form)


@router.post("/return")
async def ecpay_return(request: Request, db: Session = Depends(get_db)):
    form_data = await request.form()
    data_dict = dict(form_data)
    
    # 提取收到的驗證碼，並與我們自己計算的結果進行比對
    received_mac = data_dict.get("CheckMacValue", "")
    calculated_mac = calculate_check_mac_value(data_dict)
    
    if received_mac != calculated_mac:
        return PlainTextResponse(content="0|CheckMacValue_Error")

    merchant_trade_no = data_dict.get("MerchantTradeNo")
    rtn_code = data_dict.get("RtnCode")
    trade_amt = data_dict.get("TradeAmt")

    try:
        # 使用 with_for_update() 替這筆資料上鎖，防止綠界同時發送兩次通知導致併發 Bug
        order = db.query(models.Order).filter(models.Order.trade_no == merchant_trade_no).with_for_update().first()
        
        if not order:
            return PlainTextResponse(content="0|Order_Not_Found")

        # 嚴謹的狀態判定：必須狀態碼為 1 且 金額與資料庫完全一致
        if rtn_code == "1" and order.total_price == int(trade_amt):
            order.payment_status = "PAID"
        else:
            order.payment_status = "FAILED"
        
        db.commit() # 解除鎖定並保存
        return PlainTextResponse(content="1|OK")
        
    except Exception:
        db.rollback()
        return PlainTextResponse(content="0|DB_Error")