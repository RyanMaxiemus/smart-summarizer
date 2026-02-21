# Smart Text Summarizer (CLI)

Smart Text Summarizer is a modular Python CLI application that analyzes raw text or `.txt` files using Ollama (`kimi-k2.5:cloud`) and returns:

- A concise summary (3–5 sentences)
- Bullet point highlights
- Key topics

This project is designed to reinforce practical Python skills including:
- Modular architecture
- File handling
- Environment variable management
- API integration with `requests`
- Prompt design fundamentals
- CLI argument parsing with `argparse`
- Error handling best practices

---

## 🚀 Features

- Accepts direct text input via CLI
- Loads and processes `.txt` files
- Sends structured prompts to Ollama
- Clean and readable CLI output
- Environment-based configuration
- Expandable architecture for future upgrades

---

## 📦 Project Structure

```plain
smart_summarizer/
│
├── README.md
├── cli.py
├── summarizer.py
├── file_handler.py
├── config.py
├── utils.py
├── requirements.txt
└── .env

````

---

## 🛠 Installation

### 1. Clone the repository

```bash
git clone https://github.com/yourusername/smart-text-summarizer.git
cd smart-text-summarizer
````

### 2. Create virtual environment

```bash
python3 -m venv venv
source venv/bin/activate
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

---

## 🔐 Environment Configuration

Create a `.env` file in the project root:

```plain
OLLAMA_BASE_URL=http://localhost:11434
MODEL_NAME=kimi-k2.5:cloud
```

Make sure Ollama is installed and running locally.

---

## ▶ Usage

### Summarize text directly:

```bash
python cli.py --text "Artificial intelligence is transforming industries..."
```

### Summarize from file:

```bash
python cli.py --file example.txt
```

---

## 🧠 Learning Goals

This project demonstrates:

* Clean separation of concerns
* API request handling with `requests`
* Structured prompt engineering
* Defensive programming & error handling
* CLI UX design
* Scalable project organization

---

## 🔮 Future Improvements

* Streaming responses
* Colored CLI output (Rich)
* Logging support
* Save output to file option
* Unit tests
* Packaging as an installable CLI tool
* Web or TUI interface