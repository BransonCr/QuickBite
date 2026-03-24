import uuid
from fastapi import HTTPException

from app.schemas.Payment import Payment,PaymentCreate,PaymentUpdate,PaymentStatus
from app.models.PaymentModel import load_all,save_all 
from datetime import datetime, timezone
from app.services.OrderService import OrderService
from app.schemas.Order import OrderUpdate, OrderStatus

VALID_TRANSITIONS = {
     PaymentStatus.PENDING: [PaymentStatus.SUCCESS, PaymentStatus.FAILED],
     PaymentStatus.SUCCESS: [],
     PaymentStatus.FAILED: [PaymentStatus.PENDING]
}

class PaymentService:
     def get_all_payments(self):
        return load_all()
    
     def create_payment(self,payment:Payment) -> Payment:
          payments = load_all()

          now = datetime.now(timezone.utc)
          created_at = now.isoformat()
          if validate_card_info(payment):
               new_payment = Payment(
                    payment_id=str(uuid.uuid4()),
                    **payment.model_dump(),
                    status=PaymentStatus.PENDING,
                    created_at=created_at
               )
          payments.append(new_payment)
          save_all(payments)
          return new_payment

     def update_payment(self,payment_id:str,payment_update:PaymentUpdate) ->Payment:
          payments = load_all()
          for payment in payments:
               if payment.payment_id==payment_id:
                    if payment_update.status not in VALID_TRANSITIONS[payment.status]:
                         raise HTTPException(status_code=400,detail=f"Invalid status transition from {payment.status} to {payment_update.status}")
                    payment.status = payment_update.status
                    if payment_update.status == PaymentStatus.SUCCESS:
                         payment.confirmation_number = str(uuid.uuid4())
                         confirm_order(payment)
                    save_all(payments)
                    return payment
          raise HTTPException(status_code=404,detail="Payment not found")

     def delete_payment(self,payment_id:str):
          payments = load_all()
          for payment in payments:
               if payment.payment_id == payment_id:
                    if payment.status == PaymentStatus.SUCCESS:
                         raise HTTPException(status_code=400,detail="Cannot delete a successful payment")
                    payments.remove(payment)
                    save_all(payments)
                    return
          raise HTTPException(status_code=404,detail="Payment not found")


     def get_payment(self,payment_id:str)->Payment:
          payments = load_all()
          for payment in payments:
               if payment.payment_id ==payment_id:
                    return payment

          raise HTTPException(status_code=404,detail="Payment not found")
    
def invalid_card_number(card_num: str) -> bool:
     return card_num.strip() == "" or len(card_num) != 16 or not card_num.isdigit()
def invalid_cvv(cvv: str) -> bool:
     return cvv.strip() == "" or len(cvv) != 3 or not cvv.isdigit()
def invalid_expiration_date(expiration_date: str) -> bool:
     if expiration_date.strip() == "":
        return True
     try:
          date = datetime.strptime(expiration_date, "%m/%Y").replace(day=1)
          return date < datetime.now()
     except ValueError:
          return True

def validate_card_info(payment:PaymentCreate) -> bool:
     if invalid_card_number(payment.card_number):
          raise HTTPException(status_code=400,detail="Invalid card number")
     if invalid_cvv(payment.cvv):
          raise HTTPException(status_code=400,detail="Invalid CVV")
     if invalid_expiration_date(payment.expiration_date):
          raise HTTPException(status_code=400,detail="Invalid expiration date")
     return True

def confirm_order(payment:Payment):
     order_service = OrderService()
     update = OrderUpdate(status=OrderStatus.CONFIRMED)
     order_service.update_order(payment.order_id, update)





