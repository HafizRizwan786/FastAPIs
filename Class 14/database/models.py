from sqlmodel import SQLModel,Field,Relationship,Column
from enum import Enum
from datetime import datetime
from pydantic import EmailStr
from uuid import uuid4,UUID
from sqlalchemy.dialects import postgresql

class ShipmentStatus(str,Enum):
    placed = "placed"
    in_transit = "in_transit"
    delivered = "delivered"
    out_for_delivery = "out_for_delivery"
    

class Shipment(SQLModel,table=True):
    __tablename__="shipment" # agr ye na likhy tu wo class name ko hi lower mai change kr ky as a table name use kr leta ha by default
    id: UUID = Field(
        sa_column=Column(
            postgresql.UUID,
            default=uuid4,
            primary_key=True
        )
    )
    content: str
    weight: float = Field(le=25)
    destination: int
    status: ShipmentStatus
    estimated_delivery: datetime
    seller_id: UUID=Field(foreign_key="seller.id")
    seller: "Seller"=Relationship(
        back_populates="shipments",
        sa_relationship_kwargs={
        "lazy":"selectin"
    })


class Seller(SQLModel,table=True):
    
    id: UUID = Field(
        sa_column=Column(
            postgresql.UUID,
            default=uuid4,
            primary_key=True
        )
    )
    name: str
    email: EmailStr
    password_hash: str
    shipments: list["Shipment"]=Relationship(
        back_populates="seller",
        sa_relationship_kwargs={
        "lazy":"selectin"
    })