from fastapi import APIRouter,Depends,HTTPException,status
from api.schemas.delivery_partner import DeliveryPartnerCreate,DeliveryPartnerRead,DeliveryPartnerUpdate
from api.dependencies import DeliveryPartnerDep,get_partner_access_token,DeliveryPartnerServiceDep
from fastapi.security import OAuth2PasswordRequestForm
from typing import Annotated
from database.redis import add_jti_to_blacklist



router=APIRouter(prefix="/partner",tags=["Delivery Partner"])

# Register Delivery Partner
@router.post('/signup',response_model=DeliveryPartnerRead)
async def register_delivery_partner(seller: DeliveryPartnerCreate,service: DeliveryPartnerServiceDep):
    return await service.add(seller)


# Update Delivery Partner
@router.post('/')
async def update_delivery_partner(
    partner_update: DeliveryPartnerUpdate,
    partner: DeliveryPartnerDep,
    service: DeliveryPartnerServiceDep,
):
    # Update data with given fields
    update = partner_update.model_dump(exclude_none=True)

    if not update:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="No data provided to update",
        )

    return await service.update(
        partner.sqlmodel_update(update),
    )


# Login Delivery Partner
@router.post('/token')
async def login_delivery_partner(
        request_form: Annotated[OAuth2PasswordRequestForm,Depends()],
        service: DeliveryPartnerServiceDep
    ):
    token=await service.token(request_form.username,request_form.password)
    return {
        "access_token":token,
        "token_type":"bearer"
    }



## Logout Delivery Partner
@router.get('/logout')
async def logout_delivery_partner(
        token_data: Annotated[dict,Depends(get_partner_access_token)],
    ):
        await add_jti_to_blacklist(token_data["jti"])
        return {
            "detail": "Successfully logout"
        }


