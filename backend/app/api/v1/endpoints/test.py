from fastapi import APIRouter, HTTPException
from app.core.email import send_email, EmailSchema
from pydantic import BaseModel, EmailStr

router = APIRouter()

class TestEmail(BaseModel):
    email_to: EmailStr

@router.post("/test-email/")
async def test_email(email_data: TestEmail):
    """
    Test endpoint to verify email sending functionality
    """
    try:
        email = EmailSchema(
            email=[email_data.email_to],
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
        
        success = await send_email(email)
        if success:
            return {"message": "Test email sent successfully"}
        else:
            raise HTTPException(status_code=500, detail="Failed to send email")
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e)) 