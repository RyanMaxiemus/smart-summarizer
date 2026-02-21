import argparse
from file_handler import load_text_from_file
from summarizer import summarize_text


def main():
    parser = argparse.ArgumentParser(
        description="Smart Text Summarizer CLI"
    )

    parser.add_argument(
        "--file",
        type=str,
        help="Path to text file"
    )

    parser.add_argument(
        "--text",
        type=str,
        help="Paste text directly"
    )

    args = parser.parse_args()

    if not args.file and not args.text:
        print("Provide either --file or --text")
        return

    if args.file:
        text = load_text_from_file(args.file)
    else:
        text = args.text

    print("\nProcessing...\n")
    result = summarize_text(text)

    print("=== RESULT ===\n")
    print(result)


if __name__ == "__main__":
    main()