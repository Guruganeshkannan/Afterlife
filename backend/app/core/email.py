from typing import List, Optional
from fastapi_mail import FastMail, MessageSchema, ConnectionConfig, MessageType
from pydantic import EmailStr, BaseModel
from app.core.config import settings
import ssl
import logging
import traceback
import sys

# Set up logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.StreamHandler(sys.stdout)
    ]
)
logger = logging.getLogger(__name__)

class EmailSchema(BaseModel):
    email: List[EmailStr]
    subject: str
    body: str
    html: Optional[str] = None

# Create SSL context with proper configuration
ssl_context = ssl.create_default_context()
ssl_context.check_hostname = settings.VALIDATE_CERTS
ssl_context.verify_mode = ssl.CERT_NONE  # Disable certificate verification

# Log email configuration
logger.info(f"Email Configuration:")
logger.info(f"MAIL_USERNAME: {settings.MAIL_USERNAME}")
logger.info(f"MAIL_FROM: {settings.MAIL_FROM}")
logger.info(f"MAIL_PORT: {settings.MAIL_PORT}")
logger.info(f"MAIL_SERVER: {settings.MAIL_SERVER}")
logger.info(f"MAIL_FROM_NAME: {settings.MAIL_FROM_NAME}")
logger.info(f"MAIL_SSL_TLS: {settings.MAIL_SSL}")
logger.info(f"MAIL_STARTTLS: {settings.MAIL_TLS}")
logger.info(f"USE_CREDENTIALS: {settings.USE_CREDENTIALS}")
logger.info(f"VALIDATE_CERTS: {settings.VALIDATE_CERTS}")

conf = ConnectionConfig(
    MAIL_USERNAME=settings.MAIL_USERNAME,
    MAIL_PASSWORD=settings.MAIL_PASSWORD,
    MAIL_FROM=settings.MAIL_FROM,
    MAIL_PORT=settings.MAIL_PORT,
    MAIL_SERVER=settings.MAIL_SERVER,
    MAIL_FROM_NAME=settings.MAIL_FROM_NAME,
    MAIL_SSL_TLS=settings.MAIL_SSL,
    MAIL_STARTTLS=settings.MAIL_TLS,
    USE_CREDENTIALS=settings.USE_CREDENTIALS,
    VALIDATE_CERTS=settings.VALIDATE_CERTS,
    TEMPLATE_FOLDER=None
)

async def send_email(email: EmailSchema) -> bool:
    """
    Send an email using FastAPI-Mail
    """
    try:
        logger.info(f"Attempting to send email to {email.email}")
        logger.info(f"Using SMTP server: {settings.MAIL_SERVER}:{settings.MAIL_PORT}")
        
        message = MessageSchema(
            subject=email.subject,
            recipients=email.email,
            body=email.body,
            html=email.html or email.body,
            subtype=MessageType.html if email.html else MessageType.plain
        )
        
        fm = FastMail(conf)
        await fm.send_message(message)
        logger.info(f"Email sent successfully to {email.email}")
        return True
    except Exception as e:
        logger.error(f"Error sending email: {str(e)}")
        logger.error(f"Traceback: {traceback.format_exc()}")
        return False

async def send_message_delivery_notification(
    recipient_email: str,
    message_title: str,
    delivery_date: str
) -> bool:
    """
    Send a notification email when a message is delivered
    """
    subject = f"Your AfterLife Message '{message_title}' has been delivered"
    body = f"""
    Dear {recipient_email},

    Your AfterLife Message "{message_title}" has been delivered as scheduled on {delivery_date}.

    Best regards,
    The AfterLife Team
    """
    
    html = f"""
    <html>
        <body>
            <h2>Message Delivered</h2>
            <p>Dear {recipient_email},</p>
            <p>Your AfterLife Message "<strong>{message_title}</strong>" has been delivered as scheduled on {delivery_date}.</p>
            <p>Best regards,<br>The AfterLife Team</p>
        </body>
    </html>
    """
    
    email_schema = EmailSchema(
        email=[recipient_email],
        subject=subject,
        body=body,
        html=html
    )
    
    return await send_email(email_schema)

async def send_message_scheduled_notification(
    recipient_email: str,
    message_title: str,
    delivery_date: str
) -> bool:
    """
    Send a notification email when a message is scheduled for delivery
    """
    subject = f"Your AfterLife Message '{message_title}' has been scheduled"
    body = f"""
    Dear {recipient_email},

    Your AfterLife Message "{message_title}" has been scheduled for delivery on {delivery_date}.

    Best regards,
    The AfterLife Team
    """
    
    html = f"""
    <html>
        <body>
            <h2>Message Scheduled</h2>
            <p>Dear {recipient_email},</p>
            <p>Your AfterLife Message "<strong>{message_title}</strong>" has been scheduled for delivery on {delivery_date}.</p>
            <p>Best regards,<br>The AfterLife Team</p>
        </body>
    </html>
    """
    
    email_schema = EmailSchema(
        email=[recipient_email],
        subject=subject,
        body=body,
        html=html
    )
    
    return await send_email(email_schema) 