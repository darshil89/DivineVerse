import openai
import os
from dotenv import load_dotenv

load_dotenv()

def get_embedding(text: str) -> list[float]:
    print(f"Getting embedding for {text}")
    client = openai.OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
    response = client.embeddings.create(
        model="text-embedding-ada-002",
        input=text
    )
    return response.data[0].embedding