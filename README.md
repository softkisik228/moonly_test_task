# LangGraph Chatbot with Time Tool

This is a minimal LangGraph chatbot using a single tool `get_current_time`. It returns UTC time when the user asks for it.

## 🧪 Run Locally

```bash
git clone https://github.com/softkisik228/moonly_test_task.git
cd moonly_test_task
python -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt
langgraph dev
```

## Installing Ollama

Ollama is a local runtime for running large language models (LLMs) like openhermes directly on your machine.

```bash
curl -fsSL https://ollama.com/install.sh | sh
```

## Running openhermes Model

To download and run the openhermes model locally, use:

```bash
ollama run openhermes
```
