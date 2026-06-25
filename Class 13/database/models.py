from sqlmodel import SQLModel,Field
from enum import Enum
from datetime import datetime
from pydantic import EmailStr


class ShipmentStatus(str,Enum):
    placed = "placed"
    in_transit = "in_transit"
    delivered = "delivered"
    out_for_delivery = "out_for_delivery"
    

class Shipment(SQLModel,table=True):
    __tablename__="shipment" # agr ye na likhy tu wo class name ko hi lower mai change kr ky as a table name use kr leta ha by default
    id: int = Field(default=None,primary_key=True)
    content: str
    weight: float = Field(le=25)
    destination: int
    status: ShipmentStatus 
    estimated_delivery: datetime


class Seller(SQLModel,table=True):
    
    id: int=Field(default=None, primary_key=True)
    name: str
    email: EmailStr
    password_hash: str
    