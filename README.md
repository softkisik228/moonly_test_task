# LangGraph Chatbot with Time Tool

This is a minimal LangGraph chatbot using a single tool `get_current_time`. It returns UTC time when the user asks for it.

## 🧪 Run Locally

```bash
git clone --branch gigachat https://github.com/softkisik228/moonly_test_task.git
cd moonly_test_task
python -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt
langgraph dev
```

## 🔐 Environment Variables
To use the GigaChat model, you must set the GIGACHAT_CREDENTIALS environment variable with your credentials.

You can provide it in one of two ways:

1. Create a .env file in the project root:
```.env
GIGACHAT_CREDENTIALS=#your_gigachat_credentials_here
```
2. Or export it manually in the terminal:
```bash
export GIGACHAT_CREDENTIALS=#your_gigachat_credentials_here
```
Make sure this variable is available when you run langgraph dev, otherwise the model will not work correctly.
