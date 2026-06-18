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

class Shipment(BaseModel):
    weight: float = Field(ge=1, le=25, description="Weight of the shipment in kg")
    content: str = Field(max_length=100, description="Description of the shipment content")
    destination: int | None = Field(default_factory=get_random_dest, description="Provide destination otherwise random will be generated") 
    status: ShipmentStatus
    
    # dest: int | None =Field(default=randint(11000,11999))  es case mai ye ho ga ky sb new data ki same random destination ho gi but default factory mai diff random destination