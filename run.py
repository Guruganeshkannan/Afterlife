import os
import sys
import subprocess
import webbrowser
from threading import Thread
import time
import logging
import platform

# Set up logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

def run_backend():
    """Run the backend server"""
    try:
        backend_path = os.path.join(os.getcwd(), 'backend')
        logger.info(f"Looking for backend at: {backend_path}")
        if not os.path.exists(backend_path):
            logger.error(f"Backend directory not found at: {backend_path}")
            return
        
        os.chdir(backend_path)
        logger.info(f"Starting backend server from: {os.getcwd()}")
        
        # Add the current directory to the Python path
        sys.path.insert(0, os.getcwd())
        
        # Run the backend server
        subprocess.run([sys.executable, '-m', 'uvicorn', 'app.main:app', '--reload', '--port', '8000'])
    except Exception as e:
        logger.error(f"Failed to start backend server: {str(e)}")
        sys.exit(1)

def run_frontend():
    """Run the frontend server"""
    try:
        # Get the absolute path to the frontend directory
        frontend_path = os.path.abspath(os.path.join(os.getcwd(), 'frontend'))
        logger.info(f"Looking for frontend at: {frontend_path}")
        
        if not os.path.exists(frontend_path):
            logger.error(f"Frontend directory not found at: {frontend_path}")
            # List all directories in the current working directory to help diagnose the issue
            logger.info("Available directories in current working directory:")
            for item in os.listdir(os.getcwd()):
                if os.path.isdir(os.path.join(os.getcwd(), item)):
                    logger.info(f"  - {item}")
            return

        os.chdir(frontend_path)
        logger.info(f"Starting frontend server from: {os.getcwd()}")
        
        # Check if Node.js is installed
        try:
            subprocess.run(['node', '--version'], check=True, capture_output=True)
            logger.info("Node.js is installed")
        except (subprocess.SubprocessError, FileNotFoundError):
            logger.error("Node.js is not installed or not in PATH. Please install Node.js from https://nodejs.org/")
            return
        
        # Check if npm is installed
        try:
            subprocess.run(['npm', '--version'], check=True, capture_output=True)
            logger.info("npm is installed")
        except (subprocess.SubprocessError, FileNotFoundError):
            logger.error("npm is not installed or not in PATH. Please install Node.js from https://nodejs.org/")
            return
        
        # Check if node_modules exists
        if not os.path.exists('node_modules'):
            logger.info("Installing frontend dependencies...")
            subprocess.run(['npm', 'install'], check=True)
        
        # Start the frontend server
        logger.info("Starting npm...")
        subprocess.run(['npm', 'start'], check=True)
    except Exception as e:
        logger.error(f"Failed to start frontend server: {str(e)}")
        # Don't exit here, let the backend continue running

def open_browser():
    """Open the browser after a short delay"""
    time.sleep(5)  # Wait for servers to start
    webbrowser.open('http://localhost:3000')

if __name__ == "__main__":
    # Get the absolute path of the project root
    project_root = os.path.dirname(os.path.abspath(__file__))
    logger.info(f"Project root directory: {project_root}")
    os.chdir(project_root)  # Ensure we're in the project root
    
    # List all directories in the project root to help diagnose the issue
    logger.info("Available directories in project root:")
    for item in os.listdir(project_root):
        if os.path.isdir(os.path.join(project_root, item)):
            logger.info(f"  - {item}")
    
    # Start backend in a separate thread
    backend_thread = Thread(target=run_backend)
    backend_thread.daemon = True
    backend_thread.start()
    
    # Start frontend in a separate thread
    frontend_thread = Thread(target=run_frontend)
    frontend_thread.daemon = True
    frontend_thread.start()
    
    # Open browser in a separate thread
    browser_thread = Thread(target=open_browser)
    browser_thread.daemon = True
    browser_thread.start()
    
    try:
        # Keep the main thread alive
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        logger.info("\nShutting down servers...")
        sys.exit(0) 