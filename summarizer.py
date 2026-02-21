import requests
from config import OLLAMA_BASE_URL, MODEL_NAME


def build_prompt(text: str) -> str:
    return f"""
You are a summarization assistant.

Return your response in EXACT format:

SUMMARY:
<3-5 sentence summary>

BULLETS:
- point 1
- point 2
- point 3

TOPICS:
topic1, topic2, topic3

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