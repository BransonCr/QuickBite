import uuid
from fastapi import HTTPException

from app.schemas.Payment import Payment,PaymentCreate,PaymentUpdate,PaymentStatus
from app.models.PaymentModel import load_all,save_all 
from datetime import datetime, timezone

class PaymentService:
    def get_payments(self):
        return load_all()
    
    def create_payment(self,payment:Payment) -> Payment:
     now = datetime.now(timezone.utc)
     created_at = now.isoformat()
     if valid_card_info(payment):
          new_payment = Payment(
               payment_id=str(uuid.uuid4()),
               **payment.model_dump(),
               confirmation_number=str(uuid.uuid4()),
               status=PaymentStatus.PENDING,
               created_at=created_at
          )
          save_all([new_payment])
          return new_payment

    def update_payment(self,payment_id:str,payment_update:PaymentUpdate) ->Payment:
          payments = load_all()
          for payment in payments:
               if payment.payment_id==payment_id:
                    for k,payment_update in payment.model._dump().items():
                         setattr(payment,k,payment_update)
                    save_all(payments)
          raise HTTPException(status_code=404,detail="Payment didn't update")

    def delete_payment(self,payment_id:str):
          payments = load_all()
          for payment in payments:
               if payment.payment_id == payment_id:
                    payments.remove(payment)
                    save_all(payments)
                    return
          raise HTTPException(status_code=404,detail="Payment is not deleted")


    def get_payment(self,payment_id:str)->Payment:
          payments = load_all()
          for payment in payments:
               if payment.payment_id ==payment_id:
                    return payment

          raise HTTPException(status_code=404,detail="Payment not found")
    
def valid_card_info(payment:PaymentCreate) -> bool:
     if payment.card_number is None:
          raise HTTPException(status_code=400,detail="Card number is required")
     if len(payment.card_number) != 16 or not payment.card_number.isdigit():
          raise HTTPException(status_code=400,detail="Invalid card number")
     if payment.cvv is None:
          raise HTTPException(status_code=400,detail="CVV is required")
     if len(payment.cvv) != 3 or not payment.cvv.isdigit():
          raise HTTPException(status_code=400,detail="Invalid CVV")
     if payment.expiration_date is None:
          raise HTTPException(status_code=400,detail="Expiration date is required")
     expiration_date = datetime.strptime(payment.expiration_date, "%m/%Y")
     now = datetime.strptime(datetime.now().strftime("%m/%Y"), "%m/%Y")
     if expiration_date < now:
          raise HTTPException(status_code=400,detail="Card has expired")
     return True



