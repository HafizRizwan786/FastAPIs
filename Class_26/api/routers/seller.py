from fastapi import APIRouter,Depends,Request,Form
from Class_26.api.schemas.seller import SellerCreate,SellerRead
from Class_26.api.dependencies import SellerServiceDep,get_seller_access_token
from fastapi.security import OAuth2PasswordRequestForm
from typing import Annotated
from Class_26.database.redis import add_jti_to_blacklist
from pydantic import EmailStr
from Class_26.config import app_settings
from fastapi.templating import Jinja2Templates
from Class_26.utils import TEMPLATE_DIR



router=APIRouter(prefix="/seller",tags=["Seller"])

# Register Seller
@router.post('/signup',response_model=SellerRead)
async def register_seller(seller: SellerCreate,service: SellerServiceDep):
    return await service.add(seller)



# Login Seller
@router.post('/token')
async def login_seller(
        request_form: Annotated[OAuth2PasswordRequestForm,Depends()],
        service: SellerServiceDep
    ):
    token=await service.token(request_form.username,request_form.password)
    return {
        "access_token":token,
        "token_type":"bearer"
    }


# Verify Seller Email
@router.get("/verify")
async def verify_seller_email(token: str, service: SellerServiceDep):
    await service.verify_email(token)
    return {"detail" : "Account Verified"}


# Email Password Reset
@router.get("/forgot_password")
async def forgot_password(email: EmailStr, service: SellerServiceDep):
    await service.send_password_reset_link(email,router.prefix)
    return {"detail" : "Check email for password reset link"}


# Password Reset Form
@router.get("/reset_password_form")
async def get_reset_password_form(request: Request, token: str):
    templates = Jinja2Templates(TEMPLATE_DIR)

    return templates.TemplateResponse(
        request=request,
        name="password/reset.html",
        context={
            "reset_url": f"http://{app_settings.APP_DOMAIN}{router.prefix}/reset_password?token={token}"
        }
    )


# Reset Seller Password
@router.post("/reset_password")
async def reset_password(
    request: Request,
    token: str,
    password: Annotated[str, Form()],
    service: SellerServiceDep
    ):
    
    is_success = await service.reset_password(token, password)

    templates = Jinja2Templates(TEMPLATE_DIR)
    return templates.TemplateResponse(
        request=request,
        name="password/reset_success.html" if is_success else "password/reset_failed.html",
    )



## Logout Route
@router.get('/logout')
async def logout_seller(
        token_data: Annotated[dict,Depends(get_seller_access_token)],
    ):
        await add_jti_to_blacklist(token_data["jti"])
        return {
            "detail": "Successfully logout"
        }



# @router.get('/dashboard')
# async def get_dashboard(token: Annotated[str,Depends(oauth2_scheme)],session: SessionDep)->Seller:
#     data=decode_access_token(token)
    
#     if data is None:
#         raise HTTPException(
#             status_code=status.HTTP_401_UNAUTHORIZED,
#             detail="Invalid access token"
#         )
    
#     seller=await session.get(Seller,data['user']['id'])
    
#     return seller