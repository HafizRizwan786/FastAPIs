from services.shipment import ShipmentService
from typing import Annotated
from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession
from database.session import get_session

SessionDep=Annotated[AsyncSession,Depends(get_session)]

def get_shipment_server(session: SessionDep):
    return ShipmentService(session)

ServiceDep=Annotated[ShipmentService,Depends(get_shipment_server)]