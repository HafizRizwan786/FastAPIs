from fastapi import APIRouter,Depends,status
from Class_28.core.exceptions import NothingToUpdate
from Class_28.api.schemas.delivery_partner import DeliveryPartnerCreate,DeliveryPartnerRead,DeliveryPartnerUpdate
from Class_28.api.dependencies import DeliveryPartnerDep,get_partner_access_token,DeliveryPartnerServiceDep
from fastapi.security import OAuth2PasswordRequestForm
from typing import Annotated
from Class_28.database.redis import add_jti_to_blacklist
from Class_28.api.tag import APITag


router=APIRouter(prefix="/partner",tags=[APITag.PARTNER])

# Register Delivery Partner
@router.post('/signup',response_model=DeliveryPartnerRead)
async def register_delivery_partner(partner: DeliveryPartnerCreate,service: DeliveryPartnerServiceDep):
    return await service.add(partner)


# Verify Delivery Partner Email
@router.get("/verify")
async def verify_partner_email(token: str, service: DeliveryPartnerDep):
    await service.verify_email(token)
    return {"detail" : "Account Verified"}


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
        raise NothingToUpdate()

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


