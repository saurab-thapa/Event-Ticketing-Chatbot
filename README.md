# Event Ticketing Chatbot (Basic)

Simple Python + Streamlit chatbot for event ticketing queries.

## Stack

- Streamlit (UI)
- ScaleDown (prompt compression)
- OpenRouter (chat inference)

## Setup

1. Create and activate a virtual environment (optional)
2. Install dependencies:

   `pip install -r requirements.txt`

3. Add keys to local `.env` (auto-loaded):

   `SCALEDOWN_API_KEY=your_scaledown_key`
   `OPENROUTER_API_KEY=your_openrouter_key`
   `OPENROUTER_MODEL=your_openrouter_model`

4. Run:

   `streamlit run app.py`

## Project Structure

```
.
├── src/
│   ├── __init__.py
│   ├── config.py              # Environment config and API keys
│   ├── api/
│   │   ├── __init__.py
│   │   ├── scaledown.py       # ScaleDown compression API
│   │   └── openrouter.py      # OpenRouter chat completions API
│   └── utils/
│       ├── __init__.py
│       └── validators.py      # Topic validation and filtering
├── app.py                     # Streamlit UI entry point
├── requirements.txt           # Python dependencies
├── .env                       # API keys (DO NOT COMMIT)
├── .env.example               # Template for .env
├── README.md                  # This file
└── .gitignore                 # Git ignore rules
```

## Module Overview

- **`src/config.py`**: Loads environment variables and API keys from `.env`
- **`src/api/scaledown.py`**: Handles prompt compression via ScaleDown API
- **`src/api/openrouter.py`**: Handles chat completions via OpenRouter API
- **`src/utils/validators.py`**: Validates if user queries are event-ticketing related
- **`app.py`**: Main Streamlit UI that orchestrates the chat flow

## Current Behavior

- Accepts only event-ticketing related questions
- Rejects off-topic prompts with a clear constraint message
- Sends recent chat context to ScaleDown for compression
- Sends compressed prompt to OpenRouter for final answer
- Shows compression info (`tokens`, `successful`, `latency`, `fallback_used`)

## Notes

- If ScaleDown response does not include compressed text, app falls back to user prompt
- If keys are missing, app stops with a clear error
- This is an MVP demo (no database, auth, or real payment flow)

## Quick Test

- Allowed: `How do I book 2 tickets for an event?`
- Blocked: `How to make biryani?`
