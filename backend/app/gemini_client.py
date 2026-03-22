import os
import json
from pathlib import Path
from dotenv import load_dotenv
from google import genai

load_dotenv(dotenv_path=Path(__file__).parent.parent / '.env')

def call_gemini(prompt: str) -> dict:
    client = genai.Client(api_key=os.getenv("GEMINI_API_KEY"))
    response = client.models.generate_content(
        model="gemini-3-flash-preview",
        contents=prompt
    )
    text = response.text.strip().strip("```json").strip("```").strip()
    return json.loads(text)