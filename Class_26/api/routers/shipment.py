from Class_26.utils import TEMPLATE_DIR
from fastapi import APIRouter,status,Request,Form
from Class_26.core.exceptions import NothingToUpdate
# from fastapi.responses import HTMLResponse
from Class_26.api.schemas.shipment import ShipmentRead,ShipmentUpdate,ShipmentCreate
from Class_26.api.dependencies import ShipmentServiceDep,SellerDep,DeliveryPartnerDep,SessionDep
from Class_26.database.models import Shipment, TagName
from uuid import UUID
from fastapi.templating import Jinja2Templates
from Class_26.config import app_settings
from typing import Annotated


templates = Jinja2Templates(TEMPLATE_DIR)

router=APIRouter(prefix='/shipment',tags=['Shipment'])

# Get Method
@router.get('/',response_model=ShipmentRead)
async def get_shipment(id: UUID,service: ShipmentServiceDep):
    return await service.get(id)

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
        raise NothingToUpdate()
    
    return await service.update(id,shipment_update,partner)


# Get all shipments with a tag
@router.get("/tagged", response_model=list[ShipmentRead])
async def get_shipments_with_tag(
    tag_name: TagName,
    session: SessionDep,
):
    tag = await tag_name.tag(session)
    return tag.shipments


# add a tag to a shipment
@router.get('/tag',response_model=ShipmentRead)
async def add_tag_to_shipment(
    id: UUID,
    tag_name: TagName,
    service: ShipmentServiceDep
):
    return await service.add_tag(id,tag_name)



# Remove a tag from a shipment
@router.delete('/tag',response_model=ShipmentRead)
async def remove_tag_from_shipment(
    id: UUID,
    tag_name: TagName,
    service: ShipmentServiceDep
):
    return await service.remove_tag(id,tag_name)



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
