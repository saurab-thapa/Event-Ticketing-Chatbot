import os

import requests
import streamlit as st
from dotenv import load_dotenv

load_dotenv()

st.set_page_config(page_title="Event Ticketing Chatbot", page_icon="🎟️")

st.title("🎟️ Event Ticketing Chatbot")
st.caption("Simple Streamlit chatbot with Scaledown + OpenRouter")

model_name = os.getenv("OPENROUTER_MODEL", "stepfun/step-3.5-flash:free")
scaledown_api_key = os.getenv("SCALEDOWN_API_KEY", "")
openrouter_api_key = os.getenv("OPENROUTER_API_KEY", "")

if "messages" not in st.session_state:
    st.session_state.messages = []

if "compression_meta" not in st.session_state:
    st.session_state.compression_meta = {}


def is_event_ticketing_question(text: str) -> bool:
    topic_words = [
        "event",
        "events",
        "ticket",
        "tickets",
        "booking",
        "book",
        "buy",
        "purchase",
        "seat",
        "seats",
        "seating",
        "venue",
        "show",
        "concert",
        "conference",
        "timing",
        "date",
        "price",
        "pricing",
        "refund",
        "cancel",
        "reschedule",
        "pass",
        "entry",
    ]
    check_text = text.lower()
    return any(word in check_text for word in topic_words)


def compress_prompt(api_key: str, context_text: str, user_text: str) -> tuple[str, dict]:
    url = "https://api.scaledown.xyz/compress/raw/"
    headers = {
        "x-api-key": api_key,
        "Content-Type": "application/json",
    }
    body = {
        "context": context_text,
        "prompt": user_text,
        "scaledown": {"rate": "auto"},
    }

    response = requests.post(url, headers=headers, json=body, timeout=45)
    response.raise_for_status()
    data = response.json()

    compressed_text = (
        data.get("compressed_prompt")
        or data.get("compressed")
        or data.get("prompt")
        or (data.get("data", {}) or {}).get("compressed_prompt")
        or (data.get("result", {}) or {}).get("compressed_prompt")
        or (data.get("output", {}) or {}).get("compressed_prompt")
    )

    if not compressed_text:
        compressed_text = user_text
        data["fallback_used"] = True

    return compressed_text, data


def ask_openrouter(api_key: str, model_name: str, system_text: str, user_text: str) -> str:
    url = "https://openrouter.ai/api/v1/chat/completions"
    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json",
        "HTTP-Referer": "http://localhost",
        "X-Title": "event-ticketing-chatbot",
    }
    body = {
        "model": model_name,
        "messages": [
            {"role": "system", "content": system_text},
            {"role": "user", "content": user_text},
        ],
    }

    response = requests.post(url, headers=headers, json=body, timeout=60)
    response.raise_for_status()
    data = response.json()
    return data["choices"][0]["message"]["content"]


st.subheader("Chat")

if not scaledown_api_key or not openrouter_api_key:
    st.error("Missing keys in .env. Set SCALEDOWN_API_KEY and OPENROUTER_API_KEY.")
    st.stop()

for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.write(message["text"])

user_message = st.chat_input("Type your message here...")

if user_message:
    st.session_state.messages.append({"role": "user", "text": user_message})

    if not is_event_ticketing_question(user_message):
        bot_reply = (
            "I can only answer questions related to event ticketing. "
            "Please ask about events, tickets, booking, seats, pricing, or refunds."
        )
    else:
        try:
            recent_lines = []
            for msg in st.session_state.messages[-8:]:
                recent_lines.append(f"{msg['role']}: {msg['text']}")
            chat_context = "\n".join(recent_lines)

            compressed_prompt, compression_meta = compress_prompt(
                api_key=scaledown_api_key,
                context_text=chat_context,
                user_text=user_message,
            )
            st.session_state.compression_meta = compression_meta

            system_message = (
                "You are an event ticketing assistant only. "
                "If the user asks anything outside event ticketing, refuse briefly and "
                "ask them to stay on event ticketing topics. "
                "Keep answers short, clear, and practical."
            )
            bot_reply = ask_openrouter(
                api_key=openrouter_api_key,
                model_name=model_name,
                system_text=system_message,
                user_text=compressed_prompt,
            )
        except (requests.RequestException, KeyError, IndexError, TypeError, ValueError) as error:
            bot_reply = f"Request failed: {error}"

    st.session_state.messages.append({"role": "assistant", "text": bot_reply})
    st.rerun()

with st.expander("Compression info"):
    meta = st.session_state.compression_meta
    if meta:
        st.write(
            {
                "original_prompt_tokens": meta.get("original_prompt_tokens"),
                "compressed_prompt_tokens": meta.get("compressed_prompt_tokens"),
                "successful": meta.get("successful"),
                "latency_ms": meta.get("latency_ms"),
                "fallback_used": meta.get("fallback_used", False),
            }
        )
    else:
        st.write("No compression call yet.")
