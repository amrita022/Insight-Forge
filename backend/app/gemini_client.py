import os
import json
from pathlib import Path
from dotenv import load_dotenv
import google.generativeai as genai

load_dotenv(dotenv_path=Path(__file__).parent.parent / '.env')

def call_gemini(prompt: str) -> dict:
    genai.configure(api_key=os.getenv("GEMINI_API_KEY"))
    model = genai.GenerativeModel("gemini-1.5-flash-latest")
    response = model.generate_content(prompt)
    text = response.text.strip()
    if text.startswith("```"):
        text = text.split("```")[1]
        if text.startswith("json"):
            text = text[4:]
    return json.loads(text.strip())