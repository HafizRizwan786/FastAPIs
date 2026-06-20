from pydantic import BaseModel,Field
from random import randint
from .database.models import ShipmentStatus
from datetime import datetime


def get_random_dest():
    return randint(11000,11999)

class BaseShipment(BaseModel):
    weight: float = Field(ge=1, le=25, description="Weight of the shipment in kg")
    content: str = Field(max_length=100, description="Description of the shipment content")
    destination: int
    
class ShipmentRead(BaseShipment):
    status: ShipmentStatus
    estimated_delivery: datetime
    
class ShipmentCreate(BaseShipment):
    pass

class ShipmentUpdate(BaseModel):
    status:ShipmentStatus | None = Field(default=None)
    estimated_delivery: datetime | None =Field(default=None)