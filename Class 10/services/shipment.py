from sqlalchemy.ext.asyncio import AsyncSession
from database.models import Shipment
from api.schemas.shipment import ShipmentCreate,ShipmentUpdate
from database.models import ShipmentStatus
from datetime import datetime,timedelta

class ShipmentService:
    def __init__(self,session: AsyncSession):
        self.session=session
    
    async def get(self,id:int)->Shipment:
        return await self.session.get(Shipment,id)
    
    async def add(self,create_shipment: ShipmentCreate)->Shipment:
        new_shipment=Shipment(
            **create_shipment.model_dump(),
            status=ShipmentStatus.placed,
            estimated_delivery=datetime.now() + timedelta(days=3)
        )
        self.session.add(new_shipment)
        await self.session.commit()
        await self.session.refresh(new_shipment)
        return new_shipment
    
    async def update(self,id:int,shipment_update: dict)->Shipment:
        shipment=await self.session.get(Shipment,id)
        shipment.sqlmodel_update(shipment_update)
        
        self.session.add(shipment)
        await self.session.commit()
        await self.session.refresh(shipment)
        return shipment
    
    async def delete(self,id: int)->None:
        await self.session.delete(
            await self.session.get(Shipment,id)
        )
        await self.session.commit()