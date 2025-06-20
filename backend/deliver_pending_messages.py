import asyncio
import sys
import os
import logging

# Add the current directory to the Python path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from app.services.scheduler import check_and_deliver_messages

# Set up logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.StreamHandler(sys.stdout)
    ]
)
logger = logging.getLogger(__name__)

async def deliver_pending_messages():
    """
    Manually trigger the delivery of pending messages
    """
    logger.info("Manually triggering delivery of pending messages...")
    await check_and_deliver_messages()
    logger.info("Finished checking for pending messages.")

if __name__ == "__main__":
    asyncio.run(deliver_pending_messages()) 