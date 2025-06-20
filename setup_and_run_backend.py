import os
import sys
import subprocess
import logging
import traceback

# Set up logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

def setup_and_run_backend():
    """Install dependencies and run the backend server"""
    try:
        # Get the absolute path of the project root
        project_root = os.path.dirname(os.path.abspath(__file__))
        logger.info(f"Project root directory: {project_root}")
        
        # Path to the backend directory
        backend_path = os.path.join(project_root, 'backend')
        logger.info(f"Looking for backend at: {backend_path}")
        
        if not os.path.exists(backend_path):
            logger.error(f"Backend directory not found at: {backend_path}")
            return
        
        # Change to the backend directory
        os.chdir(backend_path)
        logger.info(f"Changed to backend directory: {os.getcwd()}")
        
        # Install dependencies
        logger.info("Installing dependencies...")
        subprocess.run([sys.executable, '-m', 'pip', 'install', '-r', 'requirements.txt'], check=True)
        
        # Add the current directory to the Python path
        sys.path.insert(0, os.getcwd())
        
        # Check if the app module exists
        try:
            import app
            logger.info("Successfully imported app module")
        except ImportError as e:
            logger.error(f"Failed to import app module: {str(e)}")
            logger.error("Available files in current directory:")
            for item in os.listdir(os.getcwd()):
                logger.info(f"  - {item}")
            return
        
        # Run the backend server
        logger.info("Starting backend server...")
        subprocess.run([sys.executable, '-m', 'uvicorn', 'app.main:app', '--reload', '--port', '8000'])
    except Exception as e:
        logger.error(f"Failed to setup and run backend server: {str(e)}")
        logger.error("Traceback:")
        logger.error(traceback.format_exc())
        sys.exit(1)

if __name__ == "__main__":
    setup_and_run_backend() 