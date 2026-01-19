# 🧠 Kaggle Solution Finder Agent

An AI-powered agent that searches, analyzes, and retrieves relevant Kaggle solutions, notebooks, and discussions to help you solve Kaggle competitions faster and more effectively.

🌐 **Live Web App (Streamlit):**  
👉 [Kaggle Solution Finder Agent – Streamlit App](https://kaggle-solution-finder-agent-khu7xeychro7gp5byrqyfw.streamlit.app)

---
Demo:

[Screen_Recording.webm](https://github.com/user-attachments/assets/b7857273-bee2-4e15-946f-0cccdc64fb76)

---

## 1. Project Title & Description

**Kaggle Solution Finder Agent**  
An intelligent search agent that ingests Kaggle-related content and answers user queries by finding relevant solutions, approaches, and insights.

![Python](https://img.shields.io/badge/python-3.12-blue)
![Package%20Manager](https://img.shields.io/badge/package%20manager-uv-purple)
![License](https://img.shields.io/badge/license-MIT-green)
![Status](https://img.shields.io/badge/status-experimental-orange)

---

## 2. Overview

Kaggle competitions often require extensive research across notebooks, discussions, and prior solutions. This project automates that process by providing an AI-powered search agent that can retrieve relevant Kaggle solutions based on natural language queries.

### Why it’s useful

- ⏱ Saves time searching through Kaggle notebooks and discussions  
- 🔍 Query-driven retrieval of relevant solutions and ideas  
- 🤖 Modular AI agent architecture  
- 📜 Automatic query logging for debugging and analysis  

### High-Level Architecture


---

## 3. Installation

### Requirements

- **Python 3.12+**
- **uv** (required)
- macOS / Linux / Windows

### Install `uv`

```bash
pip install uv
```

### Clone the Repository
```bash
git clone https://github.com/Khangtran94/Kaggle-Solution-Finder-Agent.git
cd Kaggle-Solution-Finder-Agent/app
```

### Install Dependencies
```bash
uv sync
```

## 4. Usage
⚠️ All commands must be run using uv run.

### Run the Application
```bash 
uv run python main.py
or
uv run python app.py
```

### 🌐 Web UI Mode (Streamlit)

To launch the interactive web interface locally:
```bash
uv run streamlit run app.py
```
This starts a Streamlit app where you can chat with the assistant directly in your browser.

📍 The app will be available at:
http://localhost:8501

### Data Ingestion
```bash
uv run python ingest.py
```

### Query Execution
* Agent logic: search_agent.py 
* Search utilities: search_tools.py 
* Logs saved to:
```bash
app/logs/
```

## 5. Features

* ✅ uv-based dependency management

* ✅ Modular AI search agent architecture

* ✅ Data ingestion pipeline

* ✅ Automatic JSON query logging

* ✅ Extensible search tools

Roadmap

* 🔄 Vector database integration (FAISS / Chroma)

* 🌐 Web UI / API

* 📊 Competition-aware ranking

* 🧪 Expanded tests

## 6. Contributing

1. Fork the repo

2. Create a branch
```bash
git checkout -b feature/my-feature
```
3. Commit changes
1. Open a Pull Request

Guidelines
* Follow PEP 8
* Use uv run for all commands
* Add tests where possible

## 7. Tests
```bash
uv run python ingest_test.py
```
or (future)
```bash
uv run pytest
```

## 8. Deployment (Optional)

Currently local-only.
Future options:
* Docker
* FastAPI
* GitHub Actions CI/CD

## 9. FAQ / Troubleshooting
* Import errors?

=> Run commands from app/ using uv run.

* Logs missing?

=> Ensure app/logs/ exists and is writable.

* Reset data?
```bash
uv run python ingest.py
```

## 10. Credits / Acknowledgments
* Kaggle community
* AI agent design patterns
* Python OSS ecosystem
* uv tooling

## 11. License
MIT License — see the LICENSE file.
