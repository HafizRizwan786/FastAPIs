from services.shipment import ShipmentService
from typing import Annotated
from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession
from database.session import get_session
from services.seller import SellerService

SessionDep=Annotated[AsyncSession,Depends(get_session)]


# Shipment
def get_shipment_server(session: SessionDep):
    return ShipmentService(session)

ShipmentDep=Annotated[ShipmentService,Depends(get_shipment_server)]


# Seller
def get_seller_server(session: SessionDep):
    return SellerService(session)

SellerDep=Annotated[SellerService,Depends(get_seller_server)]