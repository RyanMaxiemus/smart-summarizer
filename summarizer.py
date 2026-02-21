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

def parse_response(response: str):
    sections = {"summary": "", "bullets": [], "topics": []}

    try:
        summary_part = response.split("SUMMARY:")[1].split("BULLETS:")[0].strip()
        bullets_part = response.split("BULLETS:")[1].split("TOPICS:")[0].strip()
        topics_part = response.split("TOPICS:")[1].strip()

        sections["summary"] = summary_part
        sections["bullets"] = [
            line.replace("- ", "").strip()
            for line in bullets_part.splitlines()
            if line.startswith("-")
        ]
        sections["topics"] = [t.strip() for t in topics_part.split(",")]

    except Exception:
        raise ValueError("Unexpected AI response format.")

    return sections

def summarize_text(text: str):
    prompt = build_prompt(text)

    payload = {
        "model": MODEL_NAME,
        "prompt": prompt,
        "stream": False
    }

    response = requests.post(
        f"{OLLAMA_BASE_URL}/api/generate",
        json=payload
    )

    response.raise_for_status()
    raw_output = response.json()["response"]

    return parse_response(raw_output)