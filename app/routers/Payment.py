from fastapi import APIRouter

from app.schemas.Payment import Payment, PaymentCreate, PaymentUpdate    
from app.services.Payment_service import PaymentService
router = APIRouter(
    prefix="/payment",
    tags=["payment"],
    responses={404: {"description": "Not found"}}
)

service = PaymentService()
@router.get("/")
async def get_all_payments():
    return service.get_all_payments()


@router.get("/{payment_id}")
async def get_payment(payment_id: str):
    return service.get_payment(payment_id)


@router.post("/")
async def create_payment(payment: PaymentCreate):
    return service.create_payment(payment)


@router.put("/{payment_id}")
async def update_payment(payment_id: str, payment: PaymentUpdate):
    return service.update_payment(payment_id, payment)


@router.delete("/{payment_id}")
async def delete_payment(payment_id: str):    
    return service.delete_payment(payment_id)
