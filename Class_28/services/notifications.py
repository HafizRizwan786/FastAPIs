from fastapi_mail import FastMail, MessageSchema, ConnectionConfig
from config import notification_settings
from pydantic import EmailStr
from fastapi import BackgroundTasks
from utils import TEMPLATE_DIR
from twilio.rest import Client
from twilio.http.async_http_client import AsyncTwilioHttpClient

class NotificationService:
    def __init__(self,tasks: BackgroundTasks):
        self.tasks=tasks
        self.fastmail = FastMail(
            ConnectionConfig(
                **notification_settings.model_dump(
                    exclude=["TWILIO_SID","TWILIO_AUTH_TOKEN","TWILIO_NUMBER"]
                ),
                TEMPLATE_FOLDER=TEMPLATE_DIR
            )
        )
        
        async_http_client = AsyncTwilioHttpClient()
        self.twilio_client=Client(
            notification_settings.TWILIO_SID,
            notification_settings.TWILIO_AUTH_TOKEN,
            http_client=async_http_client
        )


    async def send_message(self, subject: str, recipients: list[EmailStr], body: str):
        self.tasks.add_task(
            self.fastmail.send_message,
            message=MessageSchema(
                subject=subject,
                recipients=recipients,
                body=body,
                subtype="plain"
            )
        )
    
    
    async def send_email_with_template(
        self,
        recipients: list[EmailStr],
        subject: str,
        context: dict,
        template_name: str,
    ):
        self.tasks.add_task(
            self.fastmail.send_message,
            message=MessageSchema(
                recipients=recipients,
                subject=subject,
                template_body=context,
                subtype="html",
            ),
            template_name=template_name,
        )
    
    async def send_sms(self,to: str,body: str):
        await self.twilio_client.messages.create_async(
            from_=notification_settings.TWILIO_NUMBER,
            to=to,
            body=body
        )
