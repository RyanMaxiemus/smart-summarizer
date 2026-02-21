import argparse
import sys

from file_handler import load_text_from_file
from summarizer import summarize_text
from utils import format_markdown


def get_input_text(file_path: str | None, direct_text: str | None) -> str:
    """
    Determines whether to load text from file or direct CLI input.
    Raises error if neither is provided.
    """
    if file_path:
        return load_text_from_file(file_path)

    if direct_text:
        return direct_text.strip()

    raise ValueError("You must provide either --file or --text.")


def save_markdown_output(content: str, output_path: str):
    """
    Saves formatted Markdown output to a file.
    """
    try:
        with open(output_path, "w", encoding="utf-8") as f:
            f.write(content)
        print(f"\nMarkdown saved to: {output_path}")
    except Exception as e:
        raise IOError(f"Failed to save file: {e}")


def main():
    parser = argparse.ArgumentParser(
        description="Smart Text Summarizer CLI"
    )

    parser.add_argument(
        "--file",
        type=str,
        help="Path to a .txt file to summarize"
    )

    parser.add_argument(
        "--text",
        type=str,
        help="Direct text input to summarize"
    )

    parser.add_argument(
        "--output",
        type=str,
        help="Optional path to save Markdown output (e.g., summary.md)"
    )

    args = parser.parse_args()

    try:
        # Get input text
        text = get_input_text(args.file, args.text)

        if not text:
            raise ValueError("Input text is empty.")

        print("\nProcessing text with AI...\n")

        # Get structured AI result
        result = summarize_text(text)

        # Format as Markdown
        markdown_output = format_markdown(
            result["summary"],
            result["bullets"],
            result["topics"]
        )

        # Print to console
        print(markdown_output)

        # Optionally save to file
        if args.output:
            save_markdown_output(markdown_output, args.output)

    except Exception as e:
        print(f"\nError: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()