from Class_26.services.shipment_event import ShipmentEventService
from Class_26.services.shipment import ShipmentService
from Class_26.services.delivery_partner import DeliveryPartnerService
from Class_26.services.seller import SellerService

from typing import Annotated
from uuid import UUID

from fastapi import Depends, status
from Class_26.core.exceptions import InvalidToken, ClientNotAuthorized
from sqlalchemy.ext.asyncio import AsyncSession

from Class_26.core.security import oauth2_scheme_seller,oauth2_scheme_partner
from Class_26.utils import decode_access_token

from Class_26.database.models import Seller,DeliveryPartner
from Class_26.database.redis import is_jti_blacklisted
from Class_26.database.session import get_session


SessionDep=Annotated[AsyncSession,Depends(get_session)]


# Access Token data Dep
async def _get_access_token(token: str,)->dict:
    data=decode_access_token(token)
    
    if data is None or await is_jti_blacklisted(data['jti']):
        raise InvalidToken()
    return data


# Seller access token data
async def get_seller_access_token(
    token: Annotated[str, Depends(oauth2_scheme_seller)],
) -> dict:
    return await _get_access_token(token)


# Delivery partner access token data
async def get_partner_access_token(
    token: Annotated[str, Depends(oauth2_scheme_partner)],
) -> dict:
    return await _get_access_token(token)


# Logged In Seller
async def get_current_seller(
    token_data: Annotated[dict, Depends(get_seller_access_token)],
    session: SessionDep,
):
    seller = await session.get(
        Seller,
        UUID(token_data["user"]["id"]),
    )

    if seller is None:
        raise ClientNotAuthorized()

    return seller


# Logged In Delivery partner
async def get_current_partner(
    token_data: Annotated[dict, Depends(get_partner_access_token)],
    session: SessionDep,
):
    partner = await session.get(
        DeliveryPartner,
        UUID(token_data["user"]["id"]),
    )

    if partner is None:
        raise ClientNotAuthorized()

    return partner


# Shipment
async def get_shipment_service(session: SessionDep):
    return ShipmentService(
        session,
        DeliveryPartnerService(session),
        ShipmentEventService(session)
    )


# Seller
async def get_seller_service(session: SessionDep):
    return SellerService(session)

# Delivery partner service dep
async def get_delivery_partner_service(session: SessionDep):
    return DeliveryPartnerService(session)



# Seller dep annotation
SellerDep=Annotated[Seller,Depends(get_current_seller)]

# Delivery partner dep annotation
DeliveryPartnerDep = Annotated[
    DeliveryPartner,
    Depends(get_current_partner),
]

# Shipment service dep annotation
ShipmentServiceDep=Annotated[ShipmentService,Depends(get_shipment_service)]

# Seller service dep annotation
SellerServiceDep=Annotated[SellerService,Depends(get_seller_service)]

# Delivery partner service dep annotaion
DeliveryPartnerServiceDep = Annotated[
    DeliveryPartnerService,
    Depends(get_delivery_partner_service),
]