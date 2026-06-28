from services.shipment import ShipmentService
from typing import Annotated
from fastapi import Depends,HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from database.session import get_session
from services.seller import SellerService
from core.security import oauth2_scheme
from utils import decode_access_token
from database.models import Seller
from database.redis import is_jti_blacklisted
from uuid import UUID

SessionDep=Annotated[AsyncSession,Depends(get_session)]


# Shipment
def get_shipment_server(session: SessionDep):
    return ShipmentService(session)

ShipmentDep=Annotated[ShipmentService,Depends(get_shipment_server)]


# Seller
def get_seller_server(session: SessionDep):
    return SellerService(session)

SellerDep=Annotated[SellerService,Depends(get_seller_server)]

# Access Token data Dep
async def get_access_token(token: Annotated[str,Depends(oauth2_scheme)],)->dict:
    data=decode_access_token(token)
    
    if data is None or await is_jti_blacklisted(data['jti']):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid or expired access token"
        )
    return data

# Logged In Seller
async def get_current_seller(
        token_data: Annotated[dict,Depends(get_access_token)],
        session: SessionDep
    ):
    return await session.get(Seller,UUID(token_data['user']['id']))

Seller2Dep=Annotated[Seller,Depends(get_current_seller)]