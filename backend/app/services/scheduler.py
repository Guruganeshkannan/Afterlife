import asyncio
import logging
from datetime import datetime
import pytz
from sqlalchemy.orm import Session
from sqlalchemy import text
from app.db.session import SessionLocal
from app.core.email import send_email, EmailSchema
from app.core.tasks import send_message_delivery_notification_background
from fastapi import BackgroundTasks
from app.core.config import settings

# Set up logging with more detailed format
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# Set timezone to IST
IST = pytz.timezone('Asia/Kolkata')

def parse_date(date_str):
    """Parse a date string into a datetime object"""
    try:
        return datetime.strptime(date_str, '%Y-%m-%d %H:%M:%S')
    except:
        try:
            return datetime.strptime(date_str, '%Y-%m-%d %H:%M:%S.%f')
        except:
            logger.error(f"Could not parse date string: {date_str}")
            return None

async def check_and_deliver_messages():
    """
    Check for messages that need to be delivered and deliver them
    """
    logger.info("Starting check for messages to deliver...")
    
    # Get a database session
    db = SessionLocal()
    try:
        # Get all undelivered messages regardless of delivery date first to see what's in the database
        result = db.execute(
            text("SELECT id, title, content, recipient_email, delivery_date, is_delivered FROM message")
        )
        all_messages = result.fetchall()
        logger.info(f"Total messages in database: {len(all_messages)}")
        for msg in all_messages:
            delivery_date = parse_date(str(msg[4])) if msg[4] else None
            logger.info(f"Message {msg[0]}: Title='{msg[1]}', Email='{msg[3]}', Date='{delivery_date}', Delivered={msg[5]}")
        
        # Now get the messages that need to be delivered
        current_time = datetime.now(IST)
        logger.info(f"Current time (IST): {current_time}")
        
        # Convert current_time to naive datetime for database comparison
        current_time_naive = current_time.replace(tzinfo=None)
        
        result = db.execute(
            text("""
                SELECT id, title, content, recipient_email, delivery_date 
                FROM message 
                WHERE is_delivered = FALSE 
                AND delivery_date <= :current_time
                AND recipient_email IS NOT NULL
            """),
            {"current_time": current_time_naive}
        )
        messages_to_deliver = result.fetchall()
        
        logger.info(f"Found {len(messages_to_deliver)} messages to deliver")
        for msg in messages_to_deliver:
            delivery_date = parse_date(str(msg[4])) if msg[4] else None
            logger.info(f"Will deliver message {msg[0]}: '{msg[1]}' to {msg[3]} (scheduled for {delivery_date})")
            await deliver_message(db, msg)
            
    except Exception as e:
        logger.error(f"Error checking for messages to deliver: {str(e)}", exc_info=True)
    finally:
        db.close()

async def deliver_message(db: Session, message_data):
    """
    Deliver a message to its recipient
    """
    message_id = message_data[0]
    title = message_data[1]
    content = message_data[2]
    recipient_email = message_data[3]
    delivery_date = parse_date(str(message_data[4])) if message_data[4] else None
    
    try:
        logger.info(f"Starting delivery of message {message_id}: '{title}' to {recipient_email}")
        
        if not recipient_email:
            logger.warning(f"Message {message_id} has no recipient email, skipping delivery")
            return
            
        # Send the message content
        email_schema = EmailSchema(
            email=[recipient_email],
            subject=f"Your AfterLife Message: {title}",
            body=content,
            html=f"""
            <html>
                <body>
                    <h2>{title}</h2>
                    <p>{content}</p>
                    <p>This message was scheduled for delivery on {delivery_date.strftime('%Y-%m-%d %H:%M:%S') if delivery_date else 'Unknown'} IST</p>
                </body>
            </html>
            """
        )
        
        # Send the email
        logger.info(f"Attempting to send email for message {message_id}")
        success = await send_email(email_schema)
        
        if success:
            logger.info(f"Successfully sent email for message {message_id} to {recipient_email}")
            
            # Mark the message as delivered
            db.execute(
                text("UPDATE message SET is_delivered = TRUE WHERE id = :id"),
                {"id": message_id}
            )
            db.commit()
            logger.info(f"Marked message {message_id} as delivered")
            
            # Only send delivery notification if enabled
            if settings.SEND_NOTIFICATION_EMAILS:
                # Create a background tasks object
                background_tasks = BackgroundTasks()
                
                # Send a delivery notification
                await send_message_delivery_notification_background(
                    background_tasks=background_tasks,
                    recipient_email=recipient_email,
                    message_title=title,
                    delivery_date=delivery_date.strftime('%Y-%m-%d %H:%M:%S') if delivery_date else 'Unknown'
                )
                logger.info(f"Sent delivery notification for message {message_id}")
            else:
                logger.info(f"Skipping delivery notification for message {message_id} (notifications disabled)")
        else:
            logger.error(f"Failed to send email for message {message_id} to {recipient_email}")
        
    except Exception as e:
        logger.error(f"Error delivering message {message_id}: {str(e)}", exc_info=True)
        # Don't mark the message as delivered if there was an error
        db.execute(
            text("UPDATE message SET is_delivered = FALSE WHERE id = :id"),
            {"id": message_id}
        )
        db.commit()

async def start_scheduler():
    """
    Start the message scheduler
    """
    logger.info("Starting message scheduler...")
    
    while True:
        try:
            await check_and_deliver_messages()
        except Exception as e:
            logger.error(f"Error in scheduler loop: {str(e)}", exc_info=True)
        
        logger.info("Waiting 60 seconds before next check...")
        await asyncio.sleep(60) 