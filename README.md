🎟 Event Ticketing Chatbot

An AI-powered event ticketing assistant built using Streamlit, ScaleDown, and OpenRouter.

This chatbot handles event-related queries, enforces strict topic boundaries, compresses chat context efficiently, and generates intelligent responses using LLM inference.

⚡ Built as an MVP demonstration of prompt compression + AI inference pipeline integration.

🚀 Features
🎯 Smart Query Handling

Accepts only event-ticketing related queries

Automatically rejects off-topic prompts

Displays a clear constraint message for invalid inputs

🧠 Context-Aware AI Responses

Sends recent conversation context to ScaleDown

Uses compressed prompt for efficient inference

Generates final answer using OpenRouter

📊 AI Diagnostics Display

Shows:

Compression token count

Compression latency

Success status

Whether fallback was used

🛡 Safe Fallback System

If ScaleDown fails to return compressed text
→ App automatically falls back to original user prompt

If API keys are missing
→ App stops with clear error message

🏗 Tech Stack
Layer	Technology
UI	Streamlit
Prompt Compression	ScaleDown API
LLM Inference	OpenRouter
Environment Management	python-dotenv
Backend Logic	Python
📂 Project Structure
.
├── app.py
├── requirements.txt
├── .env
└── README.md
⚙️ Setup Instructions
1️⃣ (Optional) Create Virtual Environment
python -m venv venv
venv\Scripts\activate   # Windows
2️⃣ Install Dependencies
pip install -r requirements.txt
3️⃣ Add API Keys in .env
SCALEDOWN_API_KEY=your_scaledown_key
OPENROUTER_API_KEY=your_openrouter_key
OPENROUTER_MODEL=your_openrouter_model
4️⃣ Run the Application
streamlit run app.py
🧪 Quick Test
✅ Allowed Query
How do I book 2 tickets for an event?
❌ Blocked Query
How to make biryani?
🔄 Current Behavior Flow

User sends query

App checks if query is event-related

Sends recent chat context to ScaleDown

Receives compressed prompt

Sends compressed prompt to OpenRouter

Displays AI-generated answer

Shows compression metadata

📌 Limitations (MVP Scope)

No database integration

No real payment gateway

No authentication system

No persistent session storage

This is a demonstration prototype focused on AI pipeline integration.

💡 Future Improvements

🎟 Event database integration

💳 Payment flow simulation

🔐 User authentication

📈 Booking analytics dashboard

🧠 Intent classification layer

📱 Deployment to Streamlit Cloud / AWS
