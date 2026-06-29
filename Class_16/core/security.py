from fastapi.security import OAuth2PasswordBearer

oauth2_scheme_seller=OAuth2PasswordBearer(tokenUrl='/seller/token')
oauth2_scheme_partner=OAuth2PasswordBearer(tokenUrl='/partner/token')



"""
from fastapi.security import HTTPBearer
from utils import decode_access_token
from fastapi import HTTPException,depends
class AccessTokenBaerer(HTTPBearer):
    async def __call__(self,request):
        auth_credentials=await super().__call__(request)
        token=auth_credentials.credentials
        token_data=decode_access_token(token)
        
        if token_data is None:
            raise HTTPException(
                status_code=401,
                detail="Not Authorized!"
            )
        
        return token_data
    
access_token_bearer=AccessTokenBaerer()
Annotated=[dict,depends(access_token_bearer)]



Ye authentication implement krny ky liay aik or method ha agr chaho tu ye b use
kr sakty ha
"""