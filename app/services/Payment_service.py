import uuid
from fastapi import HTTPException

from app.schemas.Payment import Payment,PaymentCreate,PaymentUpdate,PaymentStatus
from app.models.PaymentModel import load_all,save_all 
from datetime import datetime

class PaymentService:
    def get_payments(self):
        return load_all()
    
    def create_payment(self,payment:Payment) -> Payment:
     now = datetime.now()
     created_at = now.strftime("%Y-%m-%d %H:%M:%S")
     new_payment = Payment(
          payment_id=str(uuid.uuid4()),
          **payment.model_dump(),
          confirmation_number=str(uuid.uuid4()),
          status=PaymentStatus.PENDING,
          created_at=payment.created_at
     )
     save_all([new_payment])
     return new_payment

    def update_payment(self,payment_id:str,payment_update:PaymentUpdate) ->Payment:
          payments = load_all()
          for payment in payments:
               if payment.payment_id==payment_id:
                    for k,payment_update in payments.model._dump().items():
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



