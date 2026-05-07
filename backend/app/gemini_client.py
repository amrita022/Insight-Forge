import os
import json
import requests
from pathlib import Path
from dotenv import load_dotenv

load_dotenv(dotenv_path=Path(__file__).parent.parent / '.env')

def call_gemini(prompt: str, parse_json: bool = True) -> dict:
    """
    Call the LLM endpoint. If `parse_json` is True, expect a JSON object in the
    model response and return it as a dict. Otherwise return a dict with
    {'text': <raw text>}.
    """
    response = requests.post(
        "https://openrouter.ai/api/v1/chat/completions",
        headers={
            "Authorization": f"Bearer {os.getenv('GEMINI_API_KEY')}",
            "Content-Type": "application/json",
            "HTTP-Referer": "https://insight-forge-eta.vercel.app",
        },
        json={
            "model": "openrouter/auto",
            "messages": [{"role": "user", "content": prompt}]
        }
    )
    data = response.json()
    if "choices" not in data:
        raise Exception(f"OpenRouter error: {data}")
    text = data["choices"][0]["message"]["content"].strip()
    # Strip common code fences
    if "```json" in text:
        text = text.split("```json")[1].split("```")[0]
    elif "```" in text:
        text = text.split("```")[1].split("```")[0]

    if parse_json:
        try:
            return json.loads(text.strip())
        except Exception as e:
            raise Exception(f"Failed to parse JSON from model response: {e}\nResponse text: {text}")
    else:
        return {"text": text}
