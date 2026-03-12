import os

try:
    import pypdf
except ImportError:
    pypdf = None

try:
    import docx
except ImportError:
    docx = None

def load_text_from_file(path: str) -> str:
    try:
        ext = os.path.splitext(path)[1].lower()
        if ext == '.pdf':
            if pypdf is None:
                raise ImportError("pypdf is required for PDF extraction. Please install it.")
            reader = pypdf.PdfReader(path)
            text = []
            for page in reader.pages:
                text.append(page.extract_text() or "")
            return "\n".join(text)
        elif ext == '.docx':
            if docx is None:
                raise ImportError("python-docx is required for DOCX extraction. Please install it.")
            doc = docx.Document(path)
            return "\n".join([para.text for para in doc.paragraphs])
        else:
            with open(path, "r", encoding="utf-8") as file:
                return file.read()
    except FileNotFoundError:
        raise FileNotFoundError("File not found. Check the path.")
    except Exception as e:
        raise Exception(f"Error reading file: {e}")