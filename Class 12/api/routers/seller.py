from fastapi import APIRouter,Depends,HTTPException,status
from api.schemas.seller import SellerCreate,SellerRead
from api.dependencies import SellerDep, SessionDep
from typing import Annotated
from fastapi.security import OAuth2PasswordRequestForm
from core.security import oauth2_scheme
from utils import decode_access_token
from database.models import Seller


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