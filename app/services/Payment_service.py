import uuid
from fastapi import HTTPException

from app.schemas.Payment import Payment,PaymentCreate,PaymentUpdate,PaymentStatus
from app.models.PaymentModel import load_all,save_all 
from datetime import datetime, timezone

VALID_TRANSITIONS = {
     PaymentStatus.PENDING: [PaymentStatus.SUCCESS, PaymentStatus.FAILED],
     PaymentStatus.SUCCESS: [],
     PaymentStatus.FAILED: []
}

class PaymentService:
     def get_all_payments(self):
        return load_all()
    
     def create_payment(self,payment:Payment) -> Payment:
          payments = load_all()

          now = datetime.now(timezone.utc)
          created_at = now.isoformat()
          if valid_card_info(payment):
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
    
def check_card_number(card_num):
     return card_num is None or card_num.strip() == "" or len(card_num) != 16 or not card_num.isdigit()
def check_cvv(cvv):
     return cvv is None or cvv.strip() == "" or len(cvv) != 3 or not cvv.isdigit()
def check_expiration_date(expiration_date):
     if expiration_date is None or expiration_date.strip() == "":
          return False
     try:
          datetime.strptime(expiration_date, "%m/%Y")
     except ValueError:
          return False
     return True

def valid_card_info(payment:PaymentCreate) -> bool:
     if check_card_number(payment.card_number):
          raise HTTPException(status_code=400,detail="Invalid card number")
     if check_cvv(payment.cvv):
          raise HTTPException(status_code=400,detail="Invalid CVV")
     if check_expiration_date(payment.expiration_date):
          raise HTTPException(status_code=400,detail="Invalid expiration date")
     return True





