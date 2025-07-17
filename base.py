from openai import OpenAI
import os
from dotenv import load_dotenv

load_dotenv()

# Create a single OpenAI client instance
_openai_client = None

def get_openai_client():
    global _openai_client
    if _openai_client is None:
        _openai_client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
    return _openai_client
    