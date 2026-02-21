import requests
from config import OLLAMA_BASE_URL, MODEL_NAME


def build_prompt(text: str) -> str:
    return f"""
You are an intelligent summarization assistant.

Analyze the following text and provide:
1. A concise summary (3-5 sentences)
2. Bullet point highlights
3. Key topics (comma separated)

Text:
{text}
"""


def summarize_text(text: str) -> str:
    prompt = build_prompt(text)

    payload = {
        "model": MODEL_NAME,
        "prompt": prompt,
        "stream": False
    }

    try:
        response = requests.post(
            f"{OLLAMA_BASE_URL}/api/generate",
            json=payload
        )

        response.raise_for_status()
        return response.json()["response"]

    except requests.exceptions.RequestException as e:
        raise ConnectionError(f"API request failed: {e}")