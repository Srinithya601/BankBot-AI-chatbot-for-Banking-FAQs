import os
import time
import json
import uuid
import streamlit as st
import ollama

# -------------------------
# Storage Utils
# -------------------------

STORAGE_FILE = "chat_history.json"
FAQ_FILE = "banking_faq.json"


def load_storage():
    if not os.path.exists(STORAGE_FILE):
        return {"conversations": {}, "active_chat": None}

    with open(STORAGE_FILE, "r", encoding="utf-8") as f:
        data = json.load(f)

    fixed = {}

    for chat_id, chat in data.get("conversations", {}).items():
        if isinstance(chat, list):
            fixed[chat_id] = {
                "title": "New Chat",
                "messages": chat
            }
        else:
            fixed[chat_id] = {
                "title": chat.get("title", "New Chat"),
                "messages": chat.get("messages", [])
            }

    data["conversations"] = fixed

    if data.get("active_chat") not in data["conversations"]:
        if len(fixed) > 0:
            data["active_chat"] = list(fixed.keys())[0]
        else:
            data["active_chat"] = None

    return data


def save_storage(data):
    with open(STORAGE_FILE, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=4)


def create_new_chat(history):
    chat_id = str(uuid.uuid4())
    history["conversations"][chat_id] = {
        "title": "New Chat",
        "messages": [
            {"role": "assistant", "text": "Hello! I'm BankBot — how can I help you today?"}
        ]
    }
    history["active_chat"] = chat_id
    return history

# -------------------------
# Banking Knowledge Base
# -------------------------

if os.path.exists(FAQ_FILE):
    with open(FAQ_FILE, "r", encoding="utf-8") as f:
        BANKING_FAQ = json.load(f)
else:
    BANKING_FAQ = {}  # empty if file missing

def get_faq_answer(question: str) -> str | None:
    for q, a in BANKING_FAQ.items():
        if q.lower() in question.lower():
            return a
    return None

# -------------------------
# Banking Query Filter
# -------------------------

BANKING_KEYWORDS = [
    "bank", "loan", "account", "credit", "debit", "interest", "balance",
    "transaction", "transfer", "atm", "mortgage", "savings", "checking"
]

def is_banking_query(user_text: str) -> bool:
    text = user_text.lower()
    return any(keyword in text for keyword in BANKING_KEYWORDS)


# -------------------------
# Simple Bot Logic
# -------------------------
BANKING_SYSTEM_PROMPT = """
You are BankBot, an AI assistant specialized in banking and financial services.
Answer only questions related to banking, bank accounts, loans, credit cards, interest rates,
transactions, and other finance-related topics.
If a user asks something unrelated to banking, politely respond:
"I'm sorry, I can only answer banking-related questions."
"""

def generate_ai_reply(prompt: str) -> str:
    try:
        response = ollama.chat(
            model="llama3.2:1b",
            messages=[
                {"role": "system", "content": BANKING_SYSTEM_PROMPT},
                {"role": "user", "content": prompt}
            ],
        )
        return response["message"]["content"]
    except Exception as e:
        return f"Error from AI: {str(e)}"

        return response["message"]["content"]
    except Exception as e:
        return f"Error from AI: {str(e)}"

# -------------------------
# UI
# -------------------------

st.set_page_config(page_title="BankBot", layout="wide")

history = load_storage()

if not history["conversations"]:
    history = create_new_chat(history)
    save_storage(history)

active_chat = history["active_chat"]
chat_data = history["conversations"][active_chat]
messages = chat_data["messages"]

# -------------------------
# Sidebar – Chat History
# -------------------------


with st.sidebar:
    st.title("💬 Chat History")

    for chat_id, chat in list(history["conversations"].items()):

        # Chat row (title + 3-dot menu)
        row = st.container()
        with row:
            col1, col2 = st.columns([4, 1])

            # Chat title (Open chat)
            with col1:
                if st.button(chat["title"], key=f"open_{chat_id}"):
                    history["active_chat"] = chat_id
                    save_storage(history)
                    st.rerun()

            # 3-dot menu (⋮)
            with col2:
                if st.button("⋮", key=f"menu_{chat_id}"):
                    st.session_state[f"menu_open_{chat_id}"] = not st.session_state.get(
                        f"menu_open_{chat_id}", False
                    )
                else:
                    st.session_state.setdefault(f"menu_open_{chat_id}", False)

        # Dropdown menu actions
        if st.session_state.get(f"menu_open_{chat_id}", False):
            with st.container():
                st.write("")  # spacing
                with st.expander("Options", expanded=True):

                    # Rename Chat
                    new_title = st.text_input(
                        f"Rename chat", 
                        value=chat["title"], 
                        key=f"title_{chat_id}"
                    )
                    if st.button("Save Name", key=f"save_{chat_id}"):
                        history["conversations"][chat_id]["title"] = new_title
                        save_storage(history)
                        st.rerun()

                    # File Upload Button
                    uploaded_file = st.file_uploader(
                        "Upload File", 
                        key=f"upload_{chat_id}", 
                        accept_multiple_files=False
                    )
                    if uploaded_file:
                        st.success("File uploaded successfully!")

                    # Delete Chat
                    if st.button("Delete Chat", key=f"delete_{chat_id}"):
                        del history["conversations"][chat_id]
                        if chat_id == history["active_chat"]:
                            if history["conversations"]:
                                history["active_chat"] = list(history["conversations"].keys())[0]
                            else:
                                history = create_new_chat(history)
                        save_storage(history)
                        st.rerun()

    st.write("---")

    if st.button("➕ New Chat"):
        history = create_new_chat(history)
        save_storage(history)
        st.rerun()



# -------------------------
# Main Chat UI
# -------------------------

st.header("BankBot AI")

chat_container = st.container()


def render_messages():
    chat_container.empty()
    with chat_container:
        for msg in messages:
            bubble = st.chat_message(msg["role"])
            bubble.markdown(msg["text"])


render_messages()

# -------------------------
# Input Form
# -------------------------

with st.form("input_form", clear_on_submit=True):
    user_input = st.text_area("Message", placeholder="Ask BankBot anything...", height=80)
    submitted = st.form_submit_button("Send")

# -------------------------
# Send Message
# -------------------------

if submitted and user_input.strip():
    user_text = user_input.strip()

    if chat_data["title"] == "New Chat":
        chat_data["title"] = user_text[:30]

    # Check banking query first
    if not is_banking_query(user_text):
        assistant_text = "I'm sorry, I can only answer banking-related questions."
        messages.append({"role": "user", "text": user_text})
        messages.append({"role": "assistant", "text": assistant_text})
        save_storage(history)
        render_messages()
    else:
        messages.append({"role": "user", "text": user_text})
        save_storage(history)

        # Check FAQ first
        answer = get_faq_answer(user_text)
        if answer:
            assistant_text = answer
        else:
            assistant_text = ""
            placeholder = st.empty()
            reply = generate_ai_reply(user_text)
            for ch in reply:
                assistant_text += ch
                placeholder.markdown(assistant_text + "▌")
                time.sleep(0.01)
            placeholder.empty()

        messages.append({"role": "assistant", "text": assistant_text})
        save_storage(history)
        render_messages()
