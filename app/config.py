
import os
from dotenv import load_dotenv

load_dotenv()

GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")

CHAT_MODEL = "gemini-2.5-flash"

EMBEDDING_MODEL = "gemini-embedding-001"
