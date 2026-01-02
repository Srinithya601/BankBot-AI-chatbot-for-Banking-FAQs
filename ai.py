import ollama

SYSTEM_PROMPT = """
You are BankBot, an AI assistant specialized in banking and finance.
If a question is not related to banking, politely refuse.
"""

def generate_ai_reply(prompt: str) -> str:
    try:
        response = ollama.chat(
            model="llama3.2:1b",
            messages=[
                {"role": "system", "content": SYSTEM_PROMPT},
                {"role": "user", "content": prompt}
            ]
        )
        return response["message"]["content"]
    except Exception as e:
        return f"AI Error: {e}"
