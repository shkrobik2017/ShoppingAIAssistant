# 🛒 Grocery AI Assistant
Grocery AI Assistant is an intelligent multi-agent system designed to help users plan meals, generate shopping lists, and stay within budget using natural language — either through text or voice commands.

## 🚀 Features
🗣️ Voice and Text Input: Accepts both typed text and recorded audio (with automatic transcription).

🍽️ Meal Planning: Suggests recipes tailored to user preferences and dietary needs.

🛍️ Shopping List Generator: Selects the best-matching products for each recipe and compiles a detailed shopping list.

💸 Budget Management: Ensures the generated list fits within the user’s specified budget and retries alternatives if over budget.

⚡ Redis Caching: Speeds up responses for frequently requested plans or products.

📊 LangGraph Multi-Agent Orchestration: Uses a graph-based multi-agent workflow for complex decision-making.

🔍 LangSmith Tracing: Integrated tracing for debugging and monitoring agent interactions.

## 🛠️ Tech Stack
- Python 3.12
- FastAPI — Backend API
- Streamlit — Interactive frontend (optional)
- LangGraph / LangChain — Multi-agent orchestration
- OpenAI Whisper / Ollama / GPT — LLMs & transcription
- PostgreSQL — Database
- Tortoise ORM — Async ORM
- Redis — Caching
- Docker / Docker Compose — Containerization

## ⚙️ How to Run
### 1. Clone the repo:
```bash
    git clone https://github.com/shkrobik2017/ShoppingAIAssistant.git
```

### 2. Create .env file from env-example file and fill variables.
```bash
    cp .env.example .env
```

### 3. Start with Docker Compose:
```bash
  docker-compose up --build
```

### 4. If you use Ollama LLM, pull model you chose into image:
```bash
    docker exec -it ollama ollama pull <your-model-name>   
```

### 5. Access to App:
FastAPI Docs: http://localhost:8000/docs

Audio request UI: http://localhost:8000/api/v1/audio

Streamlit UI: http://localhost:8501

## 📌 Example MultiAgent Flow
1️⃣ User input (text or audio) →
2️⃣ Planner Agent: Generates a plan →
3️⃣ Recipe Agent: Selects recipes →
4️⃣ Product Finder Agent: Finds products →
5️⃣ Budgeting Agent: Checks budget →
6️⃣ Finalizer Agent: Generates the final message & list

## 🧪 Run Tests
To run the tests:

1️⃣ First, build and start the app using Docker.

2️⃣ Update your .env file:

Set
```bash 
REDIS_HOST=localhost
```

Set 
```bash
POSTGRES_HOST=localhost
```

3️⃣ Open a separate terminal and run:
```bash
pytest src/tests/test_praph.py
```
💡 Make sure the app and its services (Redis, Postgres) are up and running before executing tests.
