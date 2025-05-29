import os
from dotenv import load_dotenv
load_dotenv()

from openai import OpenAI

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

def extract_department(query: str) -> str:
    prompt = f"""A user has submitted the following technical issue:
    "{query}"

    Based on the content, suggest the department name (only one word, no explanation) that should handle this issue."""
    
    response = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[{"role": "user", "content": prompt}],
        temperature=0.0,
        max_tokens=6,
    )
    return response.choices[0].message.content.strip()

def extract_feature(query: str) -> str:
    prompt = f"""Extract the product or feature name being requested from this sentence:
    "{query}"

    Respond with only the name of the product or feature, nothing else."""
    
    response = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[{"role": "user", "content": prompt}],
        temperature=0.0,
        max_tokens=10,
    )
    return response.choices[0].message.content.strip()
def query_llm(prompt: str) -> str:
    response = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[{"role": "user", "content": prompt}],
        temperature=0.0,
        max_tokens=50,
    )
    return response.choices[0].message.content.strip()

