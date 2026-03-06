from fastapi import APIRouter

from app.schema.Payment import Payment, PaymentCreate, PaymentUpdate    




router = APIRouter(
    prefix="/payment", tags=["payment"], responses={404: {"description": "Not found"}}
)

@router.get("/")
async def get_all_payments():
    return{"message":"give me all payments"}

@router.post("/")
 async def create_payment(payment: PaymentCreate):
    return {"payment": payment}

@router.get("/{payment_id}")
async def get_payment(payment_id: str):
    return {"payment_id": payment_id}

@router.put("/{payment_id}")
async def update_payment(payment_id: str, payment: PaymentUpdate):
    return {"payment_id": payment_id, "payment": payment}

@router.delete("/{payment_id}")
async def delete_payment(payment_id: str):    
    return {"payment_id": payment_id}

