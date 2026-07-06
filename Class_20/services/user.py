from services.base import BaseService
from database.models import User
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from fastapi import HTTPException,status
from passlib.context import CryptContext
from utils import generate_access_token,generate_url_safe_token,decode_url_safe_token
from services.notifications import NotificationService
from fastapi import BackgroundTasks
from config import app_settings
from uuid import UUID

password_context=CryptContext(schemes=["bcrypt"])

class UserService(BaseService):
    def __init__(self,model: User,session: AsyncSession,tasks: BackgroundTasks):
        self.session=session
        self.model=model
        self.notification_service=NotificationService(tasks)
    
    
    async def _add_user(self,data: dict,router_prefix)->User:
        user=self.model(
            **data,
            password_hash=password_context.hash(data["password"])
        )
        
        
        user = await self._add(user)
        
        token=generate_url_safe_token(
            {
                # Email can be skipped as not used in our case
                # "email": user.email,
                "id": str(user.id)
            }
        )
        
        await self.notification_service.send_email_with_template(
            recipients=[user.email],
            subject="Verify Your Account With FastShip",
            context={
                "username": user.name,
                "verification_url":f"http://{app_settings.APP_DOMAIN}/{router_prefix}/verify?token={token}"
            },
            template_name="mail_email_verify.html"
        )
        
        return user


    async def verify_email(self,token: str):
        token_data= decode_url_safe_token(token)
        
        if not token_data:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQEUST,
                detail= "Invalid token"
            )
        
        user = await self._get(UUID(token_data["id"]))
        
        if not user:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="User not found or link is invalid/expired"
            )
            
        user.email_verified=True
        await self._update(user)



    async def _get_by_email(self,email)->User | None:
        return await self.session.scalar(
            select(self.model).where(self.model.email==email)
        )
        
    
    async def _generate_token(self,email,password)->str:
        user=await self._get_by_email(email)
        
        if user is None or not password_context.verify(password,user.password_hash):
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Email or password is incorrect"
            )
            
        token=generate_access_token(data={
            "user":{
                "id": str(user.id),
                "name": user.name
            }
        })
        
        return token