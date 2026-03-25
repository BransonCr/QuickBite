import uuid
from datetime import datetime, timezone
from fastapi import HTTPException

from app.models.DeliveryModel import delete_delivery as model_delete
from app.models.DeliveryModel import get_by_id, get_by_order_id, load_all, save_all
from app.schemas.Delivery import (
    Delivery,
    DeliveryCreate,
    DeliveryStatus,
    DeliveryUpdate,
)
from app.schemas.Order import OrderStatus, OrderUpdate
from app.services.OrderService import OrderService

VALID_TRANSITIONS = {
    DeliveryStatus.ASSIGNED: [DeliveryStatus.IN_TRANSIT],
    DeliveryStatus.IN_TRANSIT: [DeliveryStatus.DELIVERED],
    DeliveryStatus.DELIVERED: [],
}

class DeliveryService:
    def get_all(self):
        return load_all()

    def get_delivery(self, delivery_id: str) -> Delivery:
        delivery = get_by_id(delivery_id)
        if not delivery:
            raise HTTPException(status_code=404, detail="Delivery not found")
        return delivery

    def get_by_order_id(self, order_id: str) -> Delivery:
        delivery = get_by_order_id(order_id)
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
            created_at=datetime.now(timezone.utc).isoformat(),
            completed_at=None,
        )
        deliveries = load_all()
        deliveries.append(new_delivery)
        save_all(deliveries)
        return new_delivery

    def update_delivery(self, delivery_id: str, delivery_update: DeliveryUpdate) -> Delivery:
        deliveries = load_all()
        
        target_delivery = next((d for d in deliveries if d.delivery_id == delivery_id), None)
        if not target_delivery:
            raise HTTPException(status_code=404, detail="Delivery not found")

      
        update_data = delivery_update.model_dump(exclude_unset=True)

      
        if "status" in update_data:
            new_status = update_data["status"]
            if new_status not in VALID_TRANSITIONS.get(target_delivery.status, []):
                raise HTTPException(
                    status_code=422,
                    detail=f"Invalid status transition: {target_delivery.status} -> {new_status}",
                )
            if new_status == DeliveryStatus.DELIVERED:
                target_delivery.completed_at = datetime.now(timezone.utc).isoformat()

       
        for key, value in update_data.items():
            setattr(target_delivery, key, value)

        save_all(deliveries)
        return target_delivery

    def update_status(self, delivery_id: str, new_status: DeliveryStatus) -> Delivery:
        deliveries = load_all()
        
        target_delivery = next((d for d in deliveries if d.delivery_id == delivery_id), None)
        if not target_delivery:
            raise HTTPException(status_code=404, detail="Delivery not found")

        if new_status not in VALID_TRANSITIONS.get(target_delivery.status, []):
            raise HTTPException(
                status_code=422, 
                detail=f"Invalid status transition: {target_delivery.status} -> {new_status}"
            )

        target_delivery.status = new_status
        if new_status == DeliveryStatus.DELIVERED:
            target_delivery.completed_at = datetime.now(timezone.utc).isoformat()
            
        save_all(deliveries)

       
        order_service = OrderService()
        if new_status == DeliveryStatus.IN_TRANSIT:
            order_service.update_order(target_delivery.order_id, OrderUpdate(status=OrderStatus.OUT_FOR_DELIVERY))
        elif new_status == DeliveryStatus.DELIVERED:
            order_service.update_order(target_delivery.order_id, OrderUpdate(status=OrderStatus.DELIVERED))

        return target_delivery

    def delete_delivery(self, delivery_id: str) -> bool:
        if not model_delete(delivery_id):
            raise HTTPException(status_code=404, detail="Delivery not found")
        return True
