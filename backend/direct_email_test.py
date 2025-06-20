import smtplib
import ssl
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import os
from dotenv import load_dotenv
import logging
import sys

# Set up logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.StreamHandler(sys.stdout)
    ]
)
logger = logging.getLogger(__name__)

# Load environment variables from .env file
logger.info("Loading environment variables...")
load_dotenv()

def send_test_email():
    """
    Send a test email using smtplib directly
    """
    # Email configuration
    sender_email = os.getenv("MAIL_USERNAME")
    sender_password = os.getenv("MAIL_PASSWORD")
    receiver_email = "guruganeshkannan16@gmail.com"
    smtp_server = os.getenv("MAIL_SERVER")
    smtp_port = os.getenv("MAIL_PORT")

    # Log configuration
    logger.info("Email Configuration:")
    logger.info(f"SMTP Server: {smtp_server}")
    logger.info(f"SMTP Port: {smtp_port}")
    logger.info(f"Sender Email: {sender_email}")
    logger.info(f"Receiver Email: {receiver_email}")
    
    if not all([sender_email, sender_password, smtp_server, smtp_port]):
        logger.error("Missing required environment variables!")
        logger.error(f"MAIL_USERNAME: {'Set' if sender_email else 'Missing'}")
        logger.error(f"MAIL_PASSWORD: {'Set' if sender_password else 'Missing'}")
        logger.error(f"MAIL_SERVER: {'Set' if smtp_server else 'Missing'}")
        logger.error(f"MAIL_PORT: {'Set' if smtp_port else 'Missing'}")
        return False
    
    try:
        smtp_port = int(smtp_port)
    except (TypeError, ValueError):
        logger.error(f"Invalid SMTP port: {smtp_port}")
        return False
    
    # Create message
    message = MIMEMultipart("alternative")
    message["Subject"] = "Test Email from AfterLife Message Platform (Direct)"
    message["From"] = sender_email
    message["To"] = receiver_email
    
    # Create HTML content
    html = """
    <html>
        <body>
            <h2>Test Email (Direct)</h2>
            <p>This is a test email sent directly using smtplib.</p>
            <p>If you received this email, the email system is working correctly!</p>
        </body>
    </html>
    """
    
    # Attach HTML content
    html_part = MIMEText(html, "html")
    message.attach(html_part)
    
    # Create SSL context
    context = ssl.create_default_context()
    context.check_hostname = False
    context.verify_mode = ssl.CERT_NONE
    
    try:
        # Connect to the server and send the email
        logger.info(f"Connecting to {smtp_server}:{smtp_port}...")
        with smtplib.SMTP_SSL(smtp_server, smtp_port, context=context) as server:
            logger.info("Logging in...")
            server.login(sender_email, sender_password)
            logger.info("Sending email...")
            server.sendmail(sender_email, receiver_email, message.as_string())
            logger.info(f"Email sent successfully to {receiver_email}")
            return True
    except Exception as e:
        logger.error(f"Error sending email: {str(e)}")
        import traceback
        logger.error(f"Traceback: {traceback.format_exc()}")
        return False

if __name__ == "__main__":
    logger.info("Testing email functionality directly...")
    success = send_test_email()
    
    if success:
        logger.info("\nTest email sent successfully!")
        logger.info("Please check your email for the test message.")
    else:
        logger.error("\nFailed to send test email.")
        logger.error("Please check the logs above for more information.") 