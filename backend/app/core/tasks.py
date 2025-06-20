from typing import List
from fastapi import BackgroundTasks
from app.core.email import send_email, EmailSchema
from app.core.config import settings

async def send_email_background(
    background_tasks: BackgroundTasks,
    email_to: str,
    subject: str,
    body: str,
    html: str = None
) -> None:
    """
    Send an email in the background
    """
    email_schema = EmailSchema(
        email=[email_to],
        subject=subject,
        body=body,
        html=html
    )
    background_tasks.add_task(send_email, email_schema)

async def send_message_delivery_notification_background(
    background_tasks: BackgroundTasks,
    recipient_email: str,
    message_title: str,
    delivery_date: str
) -> None:
    """
    Send a delivery notification email in the background
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
    
    await send_email_background(
        background_tasks=background_tasks,
        email_to=recipient_email,
        subject=subject,
        body=body,
        html=html
    )

async def send_message_scheduled_notification_background(
    background_tasks: BackgroundTasks,
    recipient_email: str,
    message_title: str,
    delivery_date: str
) -> None:
    """
    Send a scheduled delivery notification email in the background
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
    
    await send_email_background(
        background_tasks=background_tasks,
        email_to=recipient_email,
        subject=subject,
        body=body,
        html=html
    ) 