import os
from openai import OpenAI
from dotenv import load_dotenv

load_dotenv()  # Loads the .env file from the current or parent directory

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

def classify_intent(query: str) -> str:
    prompt = f"""Classify the following user query into one of three categories:
    - "Technical Support"
    - "Product Feature Request"
    - "Sales Lead"

    Query: "{query}"
    Category (only one):"""

    response = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[{"role": "user", "content": prompt}],
        temperature=0.0,
        max_tokens=10,
    )
    return response.choices[0].message.content.strip()
