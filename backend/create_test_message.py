import sys
import os
from datetime import datetime, timedelta

# Add the current directory to the Python path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app.db.session import SessionLocal
from sqlalchemy import text

def create_test_message():
    """
    Create a test message scheduled for 2 minutes in the future
    """
    # Get a database session
    db = SessionLocal()
    try:
        # Calculate a future date (2 minutes from now)
        future_date = datetime.now() + timedelta(minutes=2)
        print(f"Creating test message scheduled for {future_date}")
        
        # Insert the test message
        db.execute(
            text("""
                INSERT INTO message 
                (title, content, delivery_date, is_delivered, delivery_method, recipient_email, user_id) 
                VALUES 
                (:title, :content, :delivery_date, :is_delivered, :delivery_method, :recipient_email, :user_id)
            """),
            {
                'title': 'Test Future Message',
                'content': 'This is a test message scheduled for the future.',
                'delivery_date': future_date,
                'is_delivered': False,
                'delivery_method': 'email',
                'recipient_email': 'guruganeshkannan16@gmail.com',
                'user_id': 2  # Using the user ID we found earlier
            }
        )
        db.commit()
        print("Test message created successfully!")
        
    except Exception as e:
        print(f"Error creating test message: {str(e)}")
    finally:
        db.close()

if __name__ == "__main__":
    create_test_message() 