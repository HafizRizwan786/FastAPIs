from fastapi import APIRouter,HTTPException,status
from api.schemas.shipment import ShipmentRead,ShipmentUpdate,ShipmentCreate
from api.dependencies import ShipmentServiceDep,SellerDep,DeliveryPartnerDep
from database.models import Shipment
from uuid import UUID

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
    
    shipment=await service.update(id,update)
    return shipment



# Delete Shipment
@router.delete('/')
async def del_shipment(id: UUID,service: ShipmentServiceDep) ->dict[str,str]:
    await service.delete(id)
    return {"Detail": f"Shipment with id #{id} have been deleted!"}
