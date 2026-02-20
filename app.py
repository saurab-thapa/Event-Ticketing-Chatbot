import streamlit as st

from src.config import model_name, scaledown_api_key, openrouter_api_key
from src.api.scaledown import compress_prompt
from src.api.openrouter import ask_openrouter
from src.utils.validators import is_event_ticketing_question

st.set_page_config(page_title="Event Ticketing Chatbot", page_icon="🎟️")

st.title("🎟️ Event Ticketing Chatbot")
st.caption("Simple Streamlit chatbot with Scaledown + OpenRouter")

if "messages" not in st.session_state:
    st.session_state.messages = []

if "compression_meta" not in st.session_state:
    st.session_state.compression_meta = {}


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
        except (KeyError, IndexError, TypeError, ValueError, Exception) as error:
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
