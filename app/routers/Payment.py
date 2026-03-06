from fastapi import APIRouter

from app.schema.Payment import Payment, PaymentCreate, PaymentUpdate    




router = APIRouter(
    prefix="/payment", tags=["payment"], responses={404: {"description": "Not found"}}
)

@router.post("/")
def create_payment(payment: Payment):
    return {"payment": payment}

@router.get("/{payment_id}")
def read_payment(payment_id: str):
    return {"payment_id": payment_id}

@router.put("/{payment_id}")
def update_payment(payment_id: str, payment: Payment):
    return {"payment_id": payment_id, "payment": payment}

@router.delete("/{payment_id}")
def delete_payment(payment_id: str):    
    return {"payment_id": payment_id}