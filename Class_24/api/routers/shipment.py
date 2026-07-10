from Class_24.utils import TEMPLATE_DIR
from fastapi import APIRouter,HTTPException,status,Request,Form
# from fastapi.responses import HTMLResponse
from Class_24.api.schemas.shipment import ShipmentRead,ShipmentUpdate,ShipmentCreate
from Class_24.api.dependencies import ShipmentServiceDep,SellerDep,DeliveryPartnerDep
from Class_24.database.models import Shipment
from uuid import UUID
from fastapi.templating import Jinja2Templates
from Class_24.config import app_settings
from typing import Annotated


templates = Jinja2Templates(TEMPLATE_DIR)

router=APIRouter(prefix='/shipment',tags=['Shipment'])

# Get Method
@router.get('/',response_model=ShipmentRead)
async def get_shipment(id: UUID,service: ShipmentServiceDep):
    shipment=await service.get(id)
    if shipment is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail='Given id does not exist'
        )
    return shipment


# Track shipment
@router.get('/track')
async def get_tracking(request: Request,id: UUID,service: ShipmentServiceDep):
    shipment=await service.get(id)
    
    context=shipment.model_dump()
    context["status"]=shipment.status
    context["parnter"]=shipment.delivery_partner.name
    context["timeline"]=shipment.timeline
    context["timeline"].reverse()
    
    return templates.TemplateResponse(
        request=request,
        name='track.html',
        context=context
    )


# Post Method
@router.post('/')
async def submit_shipment(
        seller: SellerDep,
        shipment: ShipmentCreate,
        service: ShipmentServiceDep
    )-> Shipment:
    return await service.add(shipment,seller)


# Update Shipment Status
@router.patch('/',response_model=ShipmentRead)
async def patch_shipment(
    id: UUID,
    shipment_update: ShipmentUpdate,
    partner: DeliveryPartnerDep,
    service: ShipmentServiceDep,
    ):
    update=shipment_update.model_dump(exclude_none=True)
    if not update:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Not update is provided"
        )
    
    

    return await service.update(id,shipment_update,partner)




# Cancel Shipment
@router.get('/cancel')
async def cancel_shipment(
    id: UUID,
    seller: SellerDep,
    service: ShipmentServiceDep):
    
    return await service.cancel(id,seller)




# Sumbit a reivew for a shipment
@router.get("/review")
async def submit_review_page(request: Request, token: str):
    return templates.TemplateResponse(
        request=request,
        name="review.html",
        context={
            "review_url": f"http://{app_settings.APP_DOMAIN}/shipment/review?token={token}",
        },
    )


# Sumbit a reivew for a shipment
@router.post("/review")
async def submit_review(
    token: str,
    rating: Annotated[int, Form(ge=1, le=5)],
    comment: Annotated[str | None, Form()],
    service: ShipmentServiceDep,
):
    await service.rate(token, rating, comment)
    return {"detail": "Review submitted"}
