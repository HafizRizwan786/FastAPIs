from sqlalchemy.ext.asyncio import AsyncSession
from database.models import Shipment,ShipmentStatus,Seller
from api.schemas.shipment import ShipmentCreate
from datetime import datetime,timedelta
from services.base import BaseService
from uuid import UUID
from services.delivery_partner import DeliveryPartnerService

class ShipmentService(BaseService):
    def __init__(self,session: AsyncSession,partner_service: DeliveryPartnerService):
        super().__init__(Shipment,session)
        self.partner_service=partner_service

    
    async def get(self,id:UUID)->Shipment | None:
        return await self._get(id)
    
    
    async def add(self,create_shipment: ShipmentCreate,seller: Seller)->Shipment:
        new_shipment=Shipment(
            **create_shipment.model_dump(),
            status=ShipmentStatus.placed,
            estimated_delivery=datetime.now() + timedelta(days=3),
            seller_id=seller.id
        )
        
        # Assign delivery partner to the shipment
        partner = await self.partner_service.assign_shipment(
            new_shipment,
        )
        # Add the delivery partner foreign key
        new_shipment.delivery_partner_id = partner.id
        
        return await self._add(new_shipment)
    
    
    async def update(self,shipment: Shipment)->Shipment:
        return await self._update(shipment)
    
    
    async def delete(self,id: int)->None:
        await self._delete(self.get(id))