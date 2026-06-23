from fastapi import APIRouter
from api.schemas.seller import SellerCreate,SellerRead
from api.dependencies import SellerDep


router=APIRouter(prefix="/seller",tags=["Seller"])

@router.post('/signup',response_model=SellerRead)
async def register_seller(seller: SellerCreate,service: SellerDep):
    return await service.add(seller)