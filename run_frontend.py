import os
import sys
import subprocess
import logging
import webbrowser
import time
from threading import Thread

# Set up logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

def find_npm_path():
    """Try to find the npm executable in common installation locations"""
    # Common Node.js installation paths on Windows
    possible_paths = [
        r"C:\Program Files\nodejs\npm.cmd",
        r"C:\Program Files (x86)\nodejs\npm.cmd",
        os.path.expanduser("~\\AppData\\Roaming\\npm\\npm.cmd"),
        os.path.expanduser("~\\AppData\\Roaming\\npm\\npm")
    ]
    
    # Check if npm is in the PATH
    try:
        subprocess.run(['npm', '--version'], check=True, capture_output=True)
        logger.info("npm is in PATH")
        return 'npm'
    except (subprocess.SubprocessError, FileNotFoundError):
        logger.info("npm is not in PATH, trying to find it in common locations")
    
    # Check common installation paths
    for path in possible_paths:
        if os.path.exists(path):
            logger.info(f"Found npm at: {path}")
            return path
    
    # If we get here, we couldn't find npm
    return None

def open_browser():
    """Open the browser after a short delay"""
    time.sleep(5)  # Wait for server to start
    webbrowser.open('http://localhost:3000')

def run_frontend():
    """Run the frontend server"""
    try:
        # Get the absolute path of the project root
        project_root = os.path.dirname(os.path.abspath(__file__))
        logger.info(f"Project root directory: {project_root}")
        
        # Path to the frontend directory
        frontend_path = os.path.join(project_root, 'frontend')
        logger.info(f"Looking for frontend at: {frontend_path}")
        
        if not os.path.exists(frontend_path):
            logger.error(f"Frontend directory not found at: {frontend_path}")
            # List all directories in the current working directory to help diagnose the issue
            logger.info("Available directories in current working directory:")
            for item in os.listdir(project_root):
                if os.path.isdir(os.path.join(project_root, item)):
                    logger.info(f"  - {item}")
            return

        # Change to the frontend directory
        os.chdir(frontend_path)
        logger.info(f"Starting frontend server from: {os.getcwd()}")
        
        # Check if Node.js is installed
        try:
            subprocess.run(['node', '--version'], check=True, capture_output=True)
            logger.info("Node.js is installed")
        except (subprocess.SubprocessError, FileNotFoundError):
            logger.error("Node.js is not installed or not in PATH. Please install Node.js from https://nodejs.org/")
            return
        
        # Find npm
        npm_path = find_npm_path()
        if not npm_path:
            logger.error("npm not found. Please install Node.js from https://nodejs.org/")
            return
        
        # Check if node_modules exists
        if not os.path.exists('node_modules'):
            logger.info("Installing frontend dependencies...")
            subprocess.run([npm_path, 'install'], check=True)
        
        # Start the frontend server
        logger.info("Starting npm...")
        subprocess.run([npm_path, 'start'], check=True)
    except Exception as e:
        logger.error(f"Failed to start frontend server: {str(e)}")
        sys.exit(1)

if __name__ == "__main__":
    # Start browser in a separate thread
    browser_thread = Thread(target=open_browser)
    browser_thread.daemon = True
    browser_thread.start()
    
    # Run the frontend
    run_frontend() 