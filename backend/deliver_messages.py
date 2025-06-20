import asyncio
import logging
from app.services.scheduler import check_and_deliver_messages

# Set up logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

async def deliver_messages():
    """
    Manually trigger message delivery
    """
    logger.info("Starting manual message delivery...")
    await check_and_deliver_messages()
    logger.info("Message delivery completed")

if __name__ == "__main__":
    asyncio.run(deliver_messages()) 