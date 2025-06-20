import logging
import sys
import os
from datetime import datetime
import pytz

# Add the current directory to the Python path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app.db.session import SessionLocal
from sqlalchemy import text

# Set up logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# Set timezone to IST
IST = pytz.timezone('Asia/Kolkata')

def parse_date(date_str):
    """Parse a date string into a datetime object"""
    if not date_str:
        return None
    try:
        return datetime.strptime(str(date_str), '%Y-%m-%d %H:%M:%S')
    except:
        try:
            return datetime.strptime(str(date_str), '%Y-%m-%d %H:%M:%S.%f')
        except:
            logger.error(f"Could not parse date string: {date_str}")
            return None

def check_scheduler_status():
    """
    Check the status of the scheduler and any pending messages
    """
    logger.info("Checking scheduler status...")
    
    # Get current time
    current_time = datetime.now(IST)
    logger.info(f"Current time (IST): {current_time}")
    
    # Get a database session
    db = SessionLocal()
    try:
        # Get all messages
        result = db.execute(
            text("SELECT id, title, content, recipient_email, delivery_date, is_delivered FROM message")
        )
        all_messages = result.fetchall()
        
        logger.info(f"Total messages in database: {len(all_messages)}")
        
        # Count pending messages
        pending_messages = [msg for msg in all_messages if not msg[5]]  # is_delivered = False
        logger.info(f"Pending messages: {len(pending_messages)}")
        
        # Count overdue messages
        current_time_naive = current_time.replace(tzinfo=None)
        overdue_messages = []
        
        for msg in pending_messages:
            delivery_date = parse_date(msg[4])
            if delivery_date and delivery_date <= current_time_naive:
                overdue_messages.append(msg)
                
        logger.info(f"Overdue messages: {len(overdue_messages)}")
        
        # Display all messages
        logger.info("All messages:")
        for msg in all_messages:
            delivery_date = parse_date(msg[4])
            delivery_date_str = delivery_date.strftime('%Y-%m-%d %H:%M:%S') if delivery_date else 'None'
            status = "Delivered" if msg[5] else "Pending"
            logger.info(f"ID: {msg[0]}, Title: '{msg[1]}', Email: {msg[3]}, Date: {delivery_date_str}, Status: {status}")
        
        # Display overdue messages
        if overdue_messages:
            logger.info("Overdue messages that should be delivered:")
            for msg in overdue_messages:
                delivery_date = parse_date(msg[4])
                delivery_date_str = delivery_date.strftime('%Y-%m-%d %H:%M:%S') if delivery_date else 'None'
                logger.info(f"ID: {msg[0]}, Title: '{msg[1]}', Email: {msg[3]}, Date: {delivery_date_str}")
        
    except Exception as e:
        logger.error(f"Error checking scheduler status: {str(e)}", exc_info=True)
    finally:
        db.close()

if __name__ == "__main__":
    check_scheduler_status() 