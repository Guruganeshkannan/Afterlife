import requests
import json

def test_email_service(email_to: str):
    """
    Test the email service by sending a test email
    """
    url = "http://localhost:8000/api/v1/test/test-email/"
    headers = {"Content-Type": "application/json"}
    data = {"email_to": email_to}

    try:
        response = requests.post(url, headers=headers, json=data)
        print(f"Status Code: {response.status_code}")
        print(f"Response: {response.json()}")
        return response.status_code == 200
    except Exception as e:
        print(f"Error: {str(e)}")
        return False

if __name__ == "__main__":
    # Test email address
    test_email = "guruganeshkannan16@gmail.com"
    
    print("Testing email service...")
    success = test_email_service(test_email)
    
    if success:
        print("\nTest email sent successfully!")
        print(f"Please check {test_email} for the test email.")
    else:
        print("\nFailed to send test email.")
        print("Please check the server logs for more information.") 