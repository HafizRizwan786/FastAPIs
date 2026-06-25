from fastapi import APIRouter,Depends
from api.schemas.seller import SellerCreate,SellerRead
from api.dependencies import SellerDep,get_access_token
from fastapi.security import OAuth2PasswordRequestForm
from typing import Annotated
from database.redis import add_jti_to_blacklist



router=APIRouter(prefix="/seller",tags=["Seller"])

# Register Seller
@router.post('/signup',response_model=SellerRead)
async def register_seller(seller: SellerCreate,service: SellerDep):
    return await service.add(seller)


# Login Seller
@router.post('/token')
async def login_seller(
        request_form: Annotated[OAuth2PasswordRequestForm,Depends()],
        service: SellerDep
    ):
    token=await service.token(request_form.username,request_form.password)
    return {
        "access_token":token,
        "token_type":"bearer"
    }



## Logout Route
@router.get('/logout')
async def logout_seller(
        token_data: Annotated[dict,Depends(get_access_token)],
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