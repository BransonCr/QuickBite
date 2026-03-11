import uuid

from fastapi import HTTPException

from app.models.DeliveryModel import delete_delivery as model_delete
from app.models.DeliveryModel import get_by_id, load_all, save_all
from app.schemas.Delivery import (
    Delivery,
    DeliveryCreate,
    DeliveryStatus,
    DeliveryUpdate,
)


class DeliveryService:
    def get_all(self):
        return load_all()

    def get_delivery(self, delivery_id: str) -> Delivery:
        delivery = get_by_id(delivery_id)
        if not delivery:
            raise HTTPException(status_code=404, detail="Delivery not found")
        return delivery

    def create_delivery(self, delivery: DeliveryCreate) -> Delivery:
        new_delivery = Delivery(
            delivery_id=str(uuid.uuid4()),
            order_id=delivery.order_id,
            driver_id=delivery.driver_id,
            status=DeliveryStatus.ASSIGNED,
            address=delivery.address,
            instructions=delivery.instructions,
        )
        deliveries = load_all()
        deliveries.append(new_delivery)
        save_all(deliveries)
        return new_delivery

    def update_delivery(self, delivery_id: str, delivery: DeliveryUpdate) -> Delivery:
        deliveries = load_all()
        for d in deliveries:
            if d.delivery_id == delivery_id:
                d.status = delivery.status
                d.driver_id = delivery.driver_id
                d.address = delivery.address
                d.instructions = delivery.instructions
                save_all(deliveries)
                return d
        raise HTTPException(status_code=404, detail="Delivery not found")

    def delete_delivery(self, delivery_id: str) -> bool:
        if not model_delete(delivery_id):
            raise HTTPException(status_code=404, detail="Delivery not found")
        return True
