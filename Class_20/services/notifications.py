from fastapi_mail import FastMail, MessageSchema, ConnectionConfig
from config import notification_settings
from pydantic import EmailStr
from fastapi import BackgroundTasks
from utils import TEMPLATE_DIR


class NotificationService:
    def __init__(self,tasks: BackgroundTasks):
        self.tasks=tasks
        self.fastmail = FastMail(
            ConnectionConfig(
                **notification_settings.model_dump(),
                TEMPLATE_FOLDER=TEMPLATE_DIR
            )
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
