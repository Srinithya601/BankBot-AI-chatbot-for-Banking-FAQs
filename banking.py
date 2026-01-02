import json
import os

FAQ_FILE = "banking_faq.json"

BANKING_KEYWORDS = [
    "bank", "loan", "account", "credit", "debit", "interest",
    "balance", "transaction", "transfer", "atm", "mortgage"
]

if os.path.exists(FAQ_FILE):
    with open(FAQ_FILE, "r", encoding="utf-8") as f:
        BANKING_FAQ = json.load(f)
else:
    BANKING_FAQ = {}

def is_banking_query(text: str) -> bool:
    return any(k in text.lower() for k in BANKING_KEYWORDS)

def get_faq_answer(question: str):
    for q, a in BANKING_FAQ.items():
        if q.lower() in question.lower():
            return a
    return None
