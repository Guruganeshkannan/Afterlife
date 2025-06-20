import asyncio
import sys
import os

# Add the current directory to the Python path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from app.core.email import send_email, EmailSchema
from pydantic import EmailStr

async def test_email_direct():
    """
    Test the email service by sending a test email directly
    """
    email_to = "guruganeshkannan16@gmail.com"
    
    email_schema = EmailSchema(
        email=[email_to],
        subject="Test Email from AfterLife Message Platform",
        body="This is a test email to verify the email sending functionality.",
        html="""
        <html>
            <body>
                <h2>Test Email</h2>
                <p>This is a test email to verify the email sending functionality.</p>
                <p>If you received this email, the email system is working correctly!</p>
            </body>
        </html>
        """
    )
    
    print(f"Sending test email to {email_to}...")
    success = await send_email(email_schema)
    
    if success:
        print("Test email sent successfully!")
        print(f"Please check {email_to} for the test email.")
    else:
        print("Failed to send test email.")
        print("Please check the logs for more information.")

if __name__ == "__main__":
    asyncio.run(test_email_direct()) 