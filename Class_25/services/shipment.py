from Class_25.services.shipment_event import ShipmentEventService
from sqlalchemy.ext.asyncio import AsyncSession
from Class_25.database.models import Shipment,ShipmentStatus,Seller,Review, TagName
from Class_25.api.schemas.shipment import ShipmentCreate, ShipmentUpdate
from datetime import datetime,timedelta
from Class_25.services.base import BaseService
from uuid import UUID
from Class_25.services.delivery_partner import DeliveryPartnerService
from fastapi import HTTPException,status
from Class_25.database.redis import get_shipment_verification_code
from Class_25.utils import decode_url_safe_token


class ShipmentService(BaseService):
    def __init__(self,session: AsyncSession,partner_service: DeliveryPartnerService,shipment_event: ShipmentEventService):
        super().__init__(Shipment,session)
        self.partner_service=partner_service
        self.shipment_event=shipment_event

    
    
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
        
        shipment = await self._add(new_shipment)
        
        event=await self.shipment_event.add(
            shipment=shipment,
            location=seller.zip_code,
            status=ShipmentStatus.placed,
            description=f"Assgined to the {partner.name}"
        )
        
        shipment.timeline.append(event)
        return shipment
    
    
    
    async def update(self,id: UUID, shipment_update: ShipmentUpdate,partner: DeliveryPartnerService)->Shipment:
        # Validate logged in parter with assigned partner
        # on the shipment with given id
        shipment = await self.get(id)

        if shipment.delivery_partner_id != partner.id:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Not authorized",
            )
            
        
        if shipment_update.status == ShipmentStatus.delivered:
            code = await get_shipment_verification_code(shipment.id)

            if code != shipment_update.verification_code:
                raise HTTPException(
                    status_code=status.HTTP_401_UNAUTHORIZED,
                    detail="Client not authorized",
                )

        update = shipment_update.model_dump(
            exclude_none=True,
            exclude=["verification_code"],
        )
        
        
        if shipment_update.estimated_delivery:
            shipment.estimated_delivery=shipment_update.estimated_delivery
        
        if len(update) > 1 or not shipment_update.estimated_delivery:
            await self.shipment_event.add(
                shipment=shipment,
                **update
            )
        
        return await self._update(shipment)
    
    
    
    async def add_tag(self,id: UUID, tag_name: TagName):
        shipment= await self.get(id)
        shipment.tags.append(await tag_name.tag(self.session))
        return await self._update(shipment)
    
    
    
    async def remove_tag(self,id: UUID, tag_name: TagName):
        shipment= await self.get(id)
        try:
            shipment.tags.remove(await tag_name.tag(self.session))
        except ValueError:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detial="Tag does not exist on shipment"
            )
        
        return await self._update(shipment)
    
    
    
    async def rate(self,token: str,rating: int,comment: str):
        token_data=decode_url_safe_token(token)
        
        if not token_data:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Not authorized"
            )

        shipment=await self.get(UUID(token_data['id']))
        new_review=Review(
            rating=rating,
            comment=comment if comment else None,
            shipment_id=shipment.id
        )
        self.session.add(new_review)
        await self.session.commit()
    
    
    
    async def cancel(self,id: UUID,seller: Seller)->Shipment:
        # Validate the seller
        shipment = await self.get(id)
        
        if shipment.seller_id != seller.id:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Not authorized",
            )
        
        # ye suggestion mai aya tha lec mai nhi krwaya gya
        if shipment.status == ShipmentStatus.delivered:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Cannot cancel a delivered shipment",
            )
        
        event=await self.shipment_event.add(
            shipment=shipment,
            location=seller.zip_code,
            status=ShipmentStatus.cancelled,
            description="Shipment cancelled by the seller"
        )
        
        shipment.timeline.append(event)
        return shipment
    
    async def delete(self,id: int)->None:
        await self._delete(self.get(id))