from typing import Sequence

from fastapi import status
from Class_26.core.exceptions import DeliveryPartnerNotAvailable
from sqlmodel import select, any_

from Class_26.api.schemas.delivery_partner import DeliveryPartnerCreate
from Class_26.database.models import DeliveryPartner, Shipment

from Class_26.services.user import UserService


class DeliveryPartnerService(UserService):
    def __init__(self, session):
        super().__init__(DeliveryPartner, session)


    async def add(self, delivery_partner: DeliveryPartnerCreate):
        return await self._add_user(delivery_partner.model_dump(),"partner")


    async def get_partner_by_zipcode(self, zipcode: int) -> Sequence[DeliveryPartner]:
        return (
            await self.session.scalars(
                select(DeliveryPartner).where(
                    zipcode == any_(DeliveryPartner.serviceable_zip_code)
                )
            )
        ).all()
    
    
    async def assign_shipment(self, shipment: Shipment):
        eligible_partners = await self.get_partner_by_zipcode(shipment.destination)
        
        for partner in eligible_partners:
            if partner.current_handling_capacity > 0:
                partner.shipments.append(shipment)
                return partner

        # If no eliglible partners found or
        # parters have reached max handling capacity
        raise DeliveryPartnerNotAvailable()


    async def update(self, partner: DeliveryPartner):
        return await self._update(partner)


    async def token(self, email, password) -> str:
        return await self._generate_token(email, password)
