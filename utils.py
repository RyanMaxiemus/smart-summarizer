def format_markdown(summary: str, bullets: list[str], topics: list[str]) -> str:
    bullet_section = "\n".join([f"- {point}" for point in bullets])
    topic_section = ", ".join(topics)

    markdown_output = f"""# Summary

{summary}

---

## Key Highlights

{bullet_section}

---

## Key Topics

{topic_section}
"""

    return markdown_output