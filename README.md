# LangGraph Chatbot with Time Tool

This is a minimal LangGraph chatbot using a single tool `get_current_time`. It returns UTC time when the user asks for it.

## 🧪 Run Locally

```bash
git clone --branch gigachat https://github.com/softkisik228/moonly_test_task.git
python -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt
langgraph dev
```