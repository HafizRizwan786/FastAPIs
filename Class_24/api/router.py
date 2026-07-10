from fastapi import APIRouter
from Class_24.api.routers import shipment,seller,delivery_partner

master_router=APIRouter()

master_router.include_router(shipment.router)
master_router.include_router(seller.router)
master_router.include_router(delivery_partner.router)