# AfterLife Message Platform

A secure and innovative platform for creating and delivering personalized messages to loved ones after passing away.

## Features

- Message Scheduling: Set messages to be delivered at specific dates
- AI Personality Cloning: AI-powered chatbot that mimics your communication style
- Life Event Triggers: Automatic message delivery based on life events
- Secure Cloud Storage: End-to-end encrypted message storage
- Multi-platform Access: Web and mobile applications

## Tech Stack

- Backend: Python (FastAPI)
- Frontend: React (Web) & React Native (Mobile)
- Database: PostgreSQL
- Storage: AWS S3
- AI: OpenAI GPT
- Authentication: JWT
- Encryption: AES-256

## Setup Instructions

1. Clone the repository
2. Install dependencies:
   ```bash
   # Backend
   cd backend
   pip install -r requirements.txt
   
   # Frontend
   cd frontend
   npm install
   
   # Mobile
   cd mobile
   npm install
   ```

3. Set up environment variables:
   - Create `.env` files in backend, frontend, and mobile directories
   - Add required API keys and configuration

4. Start the services:
   ```bash
   # Backend
   cd backend
   uvicorn main:app --reload
   
   # Frontend
   cd frontend
   npm start
   
   # Mobile
   cd mobile
   npm start
   ```

## Security Features

- End-to-end encryption for all messages
- Secure cloud storage with AWS S3
- JWT-based authentication
- Regular security audits
- GDPR compliance
- Data privacy protection

## License

MIT License 