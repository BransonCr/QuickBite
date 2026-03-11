from enum import Enum

from pydantic import BaseModel


# Enums from the schema, check M2 .puml file
class DeliveryStatus(str, Enum):
    ASSIGNED = "ASSIGNED"
    IN_PROGRESS = "IN_PROGRESS"
    DELIVERED = "DELIVERED"


class Delivery(BaseModel):
    delivery_id: str
    order_id: str
    driver_id: str
    status: DeliveryStatus
    address: str
    instructions: str


class DeliveryCreate(BaseModel):
    order_id: str
    driver_id: str
    address: str
    instructions: str


class DeliveryUpdate(BaseModel):
    status: DeliveryStatus
    driver_id: str
    address: str
    instructions: str
    completed_at: str
