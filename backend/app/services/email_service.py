from fastapi import HTTPException
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from jinja2 import Environment, FileSystemLoader
import os

class EmailService:
    def __init__(self):
        self.smtp_server = "smtp.gmail.com"
        self.smtp_port = 587
        self.sender_email = "your-email@gmail.com"  # Replace with your email
        self.sender_password = "your-app-password"  # Replace with your app password
        
        # Set up Jinja2 environment
        template_dir = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'templates')
        self.env = Environment(loader=FileSystemLoader(template_dir))

    def send_email(self, recipient_email: str, subject: str, title: str, content: str):
        try:
            # Load and render the template
            template = self.env.get_template('email_template.html')
            html_content = template.render(title=title, content=content)

            # Create message
            msg = MIMEMultipart('alternative')
            msg['Subject'] = subject
            msg['From'] = self.sender_email
            msg['To'] = recipient_email

            # Attach HTML content
            msg.attach(MIMEText(html_content, 'html'))

            # Send email
            with smtplib.SMTP(self.smtp_server, self.smtp_port) as server:
                server.starttls()
                server.login(self.sender_email, self.sender_password)
                server.send_message(msg)

            return True
        except Exception as e:
            raise HTTPException(status_code=500, detail=f"Failed to send email: {str(e)}")

    def send_test_email(self, recipient_email: str):
        return self.send_email(
            recipient_email=recipient_email,
            subject="Test Email from After Life Message Service",
            title="Test Message",
            content="This is a test email from the After Life Message Service. If you're receiving this, the email service is working correctly!"
        ) 