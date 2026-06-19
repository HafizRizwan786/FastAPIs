from pydantic import BaseModel,Field
from random import randint
from enum import Enum


class ShipmentStatus(str,Enum):
    placed = "placed"
    in_transit = "in_transit"
    delivered = "delivered"
    out_for_delivery = "out_for_delivery"

def get_random_dest():
    return randint(11000,11999)

class BaseShipment(BaseModel):
    weight: float = Field(ge=1, le=25, description="Weight of the shipment in kg")
    content: str = Field(max_length=100, description="Description of the shipment content")
    
class ShipmentRead(BaseShipment):
    status: ShipmentStatus
    
class ShipmentCreate(BaseShipment):
    pass

class ShipmentUpdate(BaseModel):
    status:ShipmentStatus