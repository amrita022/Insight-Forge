import os
import json
import re
from typing import Dict, Any
from dotenv import load_dotenv
import google.generativeai as genai

# Load environment variables from .env file in parent directory (backend/.env)
load_dotenv(os.path.join(os.path.dirname(__file__), '..', '.env'))


def call_gemini(prompt: str) -> Dict[str, Any]:
    """
    Call Google Gemini API with the given prompt.
    
    Args:
        prompt: The prompt string to send to Gemini
    
    Returns:
        Parsed JSON response as dictionary
    
    Raises:
        Exception: If API call fails or response cannot be parsed
    """
    try:
        # Get API key from environment
        api_key = os.getenv('GEMINI_API_KEY')
        if not api_key:
            raise ValueError("GEMINI_API_KEY not found in environment variables. Please set it in backend/.env")
        
        # Configure API
        genai.configure(api_key=api_key)
        
        # Initialize model
        model = genai.GenerativeModel('gemini-1.5-flash')
        
        # Call API
        response = model.generate_content(prompt)
        
        # Get response text
        response_text = response.text.strip()
        
        # Remove markdown code fences if present
        # Handle both ```json and ``` formats
        response_text = re.sub(r'```\s*json\s*', '', response_text)
        response_text = re.sub(r'```\s*', '', response_text)
        response_text = response_text.strip()
        
        # Parse JSON
        try:
            result = json.loads(response_text)
            return result
        except json.JSONDecodeError as e:
            raise ValueError(f"Failed to parse Gemini response as JSON: {str(e)}\nResponse: {response_text}")
    
    except Exception as e:
        raise Exception(f"Error calling Gemini API: {str(e)}")
