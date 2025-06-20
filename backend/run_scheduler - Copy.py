import asyncio
import logging
import sys
import os

# Add the current directory to the Python path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app.services.scheduler import start_scheduler

# Set up logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

async def run_scheduler():
    """
    Run the message scheduler
    """
    logger.info("Starting standalone message scheduler...")
    await start_scheduler()

if __name__ == "__main__":
    asyncio.run(run_scheduler()) 