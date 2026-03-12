import argparse
import os
import sys

import requests
from bs4 import BeautifulSoup
from rich.console import Console
from rich.panel import Panel
from rich.progress import Progress, SpinnerColumn, TextColumn
from rich.markdown import Markdown

from file_handler import load_text_from_file
from summarizer import summarize_text
from utils import format_markdown

console = Console()

def get_input_text(file_path: str | None, direct_text: str | None, url: str | None) -> str:
    """
    Determines whether to load text from file, URL, or direct CLI input.
    """
    if file_path:
        return load_text_from_file(file_path)

    if url:
        try:
            response = requests.get(url, timeout=30)
            response.raise_for_status()
            soup = BeautifulSoup(response.content, 'html.parser')
            paragraphs = soup.find_all(['p', 'article', 'main'])
            if paragraphs:
                text = " ".join([p.get_text() for p in paragraphs])
            else:
                text = soup.get_text()
            return text.strip()
        except Exception as e:
            raise Exception(f"Failed to scrape URL: {e}")

    if direct_text:
        return direct_text.strip()

    raise ValueError("You must provide --file, --text, or --url.")

def save_markdown_output(content: str, output_path: str):
    """
    Saves formatted Markdown output to a file.
    """
    try:
        output_dir = os.path.dirname(os.path.abspath(output_path))
        if output_dir:
            os.makedirs(output_dir, exist_ok=True)
            
        with open(output_path, "w", encoding="utf-8") as f:
            f.write(content)
        console.print(f"[green]✔ Markdown saved to: [bold]{output_path}[/bold][/green]")
    except Exception as e:
        raise IOError(f"Failed to save file: {e}")

def main():
    parser = argparse.ArgumentParser(
        description="Smart Text Summarizer CLI"
    )

    parser.add_argument(
        "--file",
        type=str,
        help="Path to a file (.txt, .pdf, .docx) to summarize"
    )

    parser.add_argument(
        "--text",
        type=str,
        help="Direct text input to summarize"
    )

    parser.add_argument(
        "--url",
        type=str,
        help="URL of an article to scrape and summarize"
    )

    parser.add_argument(
        "--mode",
        type=str,
        default="default",
        choices=["default", "eli5", "executive", "technical"],
        help="Summarization persona/mode"
    )

    parser.add_argument(
        "--output",
        type=str,
        help="Optional path to save Markdown output (e.g., summary.md)"
    )

    args = parser.parse_args()

    try:
        with Progress(
            SpinnerColumn(),
            TextColumn("[progress.description]{task.description}"),
            transient=True,
            console=console,
        ) as progress:
            progress.add_task(description="Extracting text...", total=None)
            text = get_input_text(args.file, args.text, args.url)

            if not text:
                raise ValueError("Input text is empty.")

            progress.add_task(description="Processing text with AI...", total=None)
            result = summarize_text(text, mode=args.mode)

        markdown_output = format_markdown(
            result.get("summary", ""),
            result.get("bullets", []),
            result.get("topics", [])
        )

        console.print(Panel(Markdown(markdown_output), title="Smart Summarizer Output", border_style="blue"))

        if args.output:
            save_markdown_output(markdown_output, args.output)

    except Exception as e:
        console.print(f"[red]Error: {e}[/red]")
        sys.exit(1)

if __name__ == "__main__":
    main()