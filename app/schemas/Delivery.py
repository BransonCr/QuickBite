from enum import Enum

from pydantic import BaseModel
from typing import Optional


# Enums from the schema, check M2 .puml file
class DeliveryStatus(str, Enum):
    ASSIGNED = "ASSIGNED"
    IN_TRANSIT = "IN_TRANSIT"
    DELIVERED = "DELIVERED"


class Delivery(BaseModel):
    delivery_id: str
    order_id: str
    driver_id: str
    status: DeliveryStatus
    address: str
    instructions: str
    created_at: str
    completed_at: Optional[str]


class DeliveryCreate(BaseModel):
    order_id: str
    driver_id: str
    address: str
    instructions: str | None


class DeliveryUpdate(BaseModel):
    status: Optional[DeliveryStatus]
    driver_id: Optional[str]
    address: Optional[str]
    instructions: Optional[str]
