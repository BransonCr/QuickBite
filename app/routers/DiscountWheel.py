from fastapi import APIRouter, Depends

from app.schemas.DiscountWheel import SpinResult, WheelStatus
from app.services.DiscountWheelService import DiscountWheelService

router = APIRouter(
    prefix="/wheel",
    tags=["discount-wheel"],
    responses={404: {"description": "Not found"}}
)


@router.get("/status/{user_id}", response_model=WheelStatus)
async def get_wheel_status(user_id: str, service: DiscountWheelService = Depends()):
    return service.get_status(user_id)


@router.post("/spin/{user_id}", response_model=SpinResult)
async def spin_wheel(user_id: str, service: DiscountWheelService = Depends()):
    return service.spin(user_id)


@router.post("/redeem/{user_id}/{code}")
async def redeem_code(user_id: str, code: str, service: DiscountWheelService = Depends()):
    return service.redeem(user_id, code)