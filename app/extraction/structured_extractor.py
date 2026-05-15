
from google import genai

from app.config import (
    GEMINI_API_KEY,
    CHAT_MODEL
)

client = genai.Client(
    api_key=GEMINI_API_KEY
)

def extract_structured_data(text):

    prompt = f"""
Extract the following information
from this legal document.

Return VALID JSON ONLY.

FIELDS:

- parties
- dates
- obligations
- notices
- addresses

DOCUMENT:

{text}
"""

    response = client.models.generate_content(
        model=CHAT_MODEL,
        contents=prompt
    )

    return response.text
