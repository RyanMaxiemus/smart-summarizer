import json
import requests
from config import OLLAMA_BASE_URL, OLLAMA_MODEL


def build_prompt(text: str, mode: str = "default") -> str:
    if mode == "eli5":
        persona = "You are an expert at explaining complex topics to a 5-year-old in simple, fun terms."
    elif mode == "executive":
        persona = "You are a ruthless executive assistant. You focus only on action items, risks, and high-level strategy."
    elif mode == "technical":
        persona = "You are a senior technical architect analyzing the text for architectural patterns, technical depth, and implementation details."
    else:
        persona = "You are a summarization assistant."

    return f"""
{persona}

Please summarize the text and return the result strictly as a JSON object with the following keys:
- "summary": A 3-5 sentence summary of the text matching your persona.
- "bullets": A list of strings, each representing a key point matching your persona.
- "topics": A list of strings representing the main topics discussed.

Do not include any Markdown formatting or extra text.

Text:
{text}
"""

def parse_response(response: str):
    try:
        data = json.loads(response)
        
        sections = {
            "summary": data.get("summary", ""),
            "bullets": data.get("bullets", []),
            "topics": data.get("topics", [])
        }
        return sections
    except json.JSONDecodeError:
        raise ValueError("Unexpected AI response format: JSON parsing failed.")
    except Exception as e:
        raise ValueError(f"Error parsing AI response: {e}")

def chunk_text(text: str, max_words: int = 1500) -> list[str]:
    words = text.split()
    chunks = []
    current_chunk = []
    for word in words:
        current_chunk.append(word)
        if len(current_chunk) >= max_words:
            chunks.append(" ".join(current_chunk))
            current_chunk = []
    if current_chunk:
        chunks.append(" ".join(current_chunk))
    return chunks

def _summarize_chunk(text: str, mode: str = "default"):
    prompt = build_prompt(text, mode=mode)

    payload = {
        "model": OLLAMA_MODEL,
        "prompt": prompt,
        "format": "json",
        "stream": False
    }

    response = requests.post(
        f"{OLLAMA_BASE_URL}/api/generate",
        json=payload,
        timeout=120
    )

    response.raise_for_status()
    raw_output = response.json()["response"]

    return parse_response(raw_output)

def summarize_text(text: str, mode: str = "default"):
    chunks = chunk_text(text)
    
    if len(chunks) == 1:
        return _summarize_chunk(chunks[0], mode=mode)
    
    chunk_summaries = []
    for i, chunk in enumerate(chunks):
        res = _summarize_chunk(chunk, mode=mode)
        chunk_summaries.append(res.get("summary", ""))
        
    combined_text = "\n\n".join(chunk_summaries)
    return _summarize_chunk(combined_text, mode=mode)