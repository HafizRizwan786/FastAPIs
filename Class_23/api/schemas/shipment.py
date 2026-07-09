from pydantic import BaseModel,Field
from database.models import ShipmentEvent, ShipmentStatus
from datetime import datetime
from uuid import UUID
from database.models import Seller
from pydantic import EmailStr

class BaseShipment(BaseModel):
    weight: float = Field(ge=1, le=25, description="Weight of the shipment in kg")
    content: str = Field(max_length=100, description="Description of the shipment content")
    destination: int
    
class ShipmentRead(BaseShipment):
    id: UUID
    seller: Seller
    timeline: list[ShipmentEvent]
    estimated_delivery: datetime
    
class ShipmentCreate(BaseShipment):
    client_contact_email: EmailStr
    client_contact_number: str | None = Field(default=None)

class ShipmentUpdate(BaseModel):
    location: int | None =Field(default=None)
    status:ShipmentStatus | None = Field(default=None)
    verification_code: str | None = Field(default=None)
    description: str | None =Field(default=None)
    estimated_delivery: datetime | None =Field(default=None)

class ShipmentReview(BaseShipment):
    rating: int= Field(ge=1,le=5)
    comment: str | None = Field(default=None)