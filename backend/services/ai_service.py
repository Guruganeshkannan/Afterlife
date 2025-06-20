import openai
from typing import Dict, Any, List
from ..core.config import settings
from ..models.models import Message, PersonalityProfile

openai.api_key = settings.OPENAI_API_KEY

async def train_personality_profile(profile: PersonalityProfile, training_data: Dict[str, Any]) -> None:
    """
    Train the AI model on user's personality based on provided training data
    """
    # Process training data and update personality profile
    writing_samples = training_data.get("writing_samples", [])
    speech_samples = training_data.get("speech_samples", [])
    
    # Analyze writing style
    writing_style = await analyze_writing_style(writing_samples)
    
    # Analyze speech patterns
    speech_patterns = await analyze_speech_patterns(speech_samples)
    
    # Extract personality traits
    personality_traits = await extract_personality_traits(writing_samples + speech_samples)
    
    # Update profile
    profile.writing_style = writing_style
    profile.speech_patterns = speech_patterns
    profile.personality_traits = personality_traits
    profile.training_data = training_data
    profile.is_trained = True

async def analyze_writing_style(samples: List[str]) -> str:
    """
    Analyze writing style using GPT
    """
    prompt = f"""
    Analyze the following writing samples and describe the writing style:
    {' '.join(samples[:5])}  # Limit to first 5 samples for token limit
    """
    
    response = await openai.ChatCompletion.create(
        model="gpt-4",
        messages=[
            {"role": "system", "content": "You are a writing style analyzer."},
            {"role": "user", "content": prompt}
        ]
    )
    
    return response.choices[0].message.content

async def analyze_speech_patterns(samples: List[str]) -> str:
    """
    Analyze speech patterns using GPT
    """
    prompt = f"""
    Analyze the following speech samples and describe the speech patterns:
    {' '.join(samples[:5])}  # Limit to first 5 samples for token limit
    """
    
    response = await openai.ChatCompletion.create(
        model="gpt-4",
        messages=[
            {"role": "system", "content": "You are a speech pattern analyzer."},
            {"role": "user", "content": prompt}
        ]
    )
    
    return response.choices[0].message.content

async def extract_personality_traits(samples: List[str]) -> Dict[str, float]:
    """
    Extract personality traits using GPT
    """
    prompt = f"""
    Analyze the following samples and extract key personality traits:
    {' '.join(samples[:5])}  # Limit to first 5 samples for token limit
    """
    
    response = await openai.ChatCompletion.create(
        model="gpt-4",
        messages=[
            {"role": "system", "content": "You are a personality trait analyzer."},
            {"role": "user", "content": prompt}
        ]
    )
    
    # Convert response to personality traits dictionary
    traits = {
        "openness": 0.0,
        "conscientiousness": 0.0,
        "extraversion": 0.0,
        "agreeableness": 0.0,
        "neuroticism": 0.0
    }
    
    # Parse GPT response to update traits
    # This is a simplified version - in production, implement more sophisticated parsing
    return traits

async def generate_ai_response(profile: PersonalityProfile, message: str) -> str:
    """
    Generate AI response based on personality profile
    """
    system_prompt = f"""
    You are an AI assistant mimicking the personality of someone with the following traits:
    Writing style: {profile.writing_style}
    Speech patterns: {profile.speech_patterns}
    Personality traits: {profile.personality_traits}
    
    Respond to messages in a way that matches this personality profile.
    """
    
    response = await openai.ChatCompletion.create(
        model="gpt-4",
        messages=[
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": message}
        ]
    )
    
    return response.choices[0].message.content

async def deliver_message(message: Message, decrypted_content: str) -> None:
    """
    Deliver a message to the recipient
    """
    # In a production environment, implement actual message delivery
    # This could include:
    # 1. Sending emails
    # 2. Push notifications
    # 3. SMS
    # 4. Integration with messaging platforms
    
    # For now, we'll just print the message
    print(f"Delivering message: {message.title}")
    print(f"Content: {decrypted_content}")
    print(f"To recipient: {message.recipient_id}")
    
    # If this is an AI-interactive message, generate a response
    if message.sender.personality_profile and message.sender.personality_profile.is_trained:
        ai_response = await generate_ai_response(
            message.sender.personality_profile,
            decrypted_content
        )
        print(f"AI Response: {ai_response}") 