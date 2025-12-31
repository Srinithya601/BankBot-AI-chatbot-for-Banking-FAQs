# 🏦 BankBot – Streamlit AI Banking Assistant

BankBot is an interactive chatbot built using **Streamlit** and **Ollama (Llama model)**.  
It is designed to answer **banking-related questions only**, such as loans, accounts, credit cards, transactions, and interest rates.

---

## 🚀 Features

- 💬 Multi-chat support with local JSON history  
- 🧠 AI responses powered by Ollama – model: `llama3.2:1b`  
- 📑 FAQ lookup – answers common banking queries instantly  
- 🧹 Filters non-banking questions and responds politely  
- 📎 Upload button inside chat options (future extension)  
- 🗂 Rename, delete, and switch between previous conversations  

---

## 🧰 Folder Contents
.
├── app.py # Main Streamlit app
├── chat_history.json # Stores saved chats (auto-generated)
├── README.md # Documentation


> NOTE: `chat_history.json` will be created automatically on first run.

---

## How to Run Locally

### 1️⃣ Install Dependencies
```bash
pip install streamlit ollama json

2️⃣ Start Ollama Server

Download Ollama and pull the model:

ollama pull llama3.2:1b

3️⃣ Launch the App

streamlit run app.py

Then open your browser at:

👉 http://localhost:8501