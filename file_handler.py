def load_text_from_file(path: str) -> str:
    try:
        with open(path, "r", encoding="utf-8") as file:
            return file.read()
    except FileNotFoundError:
        raise FileNotFoundError("File not found. Check the path.")
    except Exception as e:
        raise Exception(f"Error reading file: {e}")