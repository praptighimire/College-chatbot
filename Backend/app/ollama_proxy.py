import requests
import json
import re

OLLAMA_URL = "http://localhost:11434/api/generate"
OLLAMA_MODEL = "gemma:2b"

# ---------------- SYSTEM PROMPT ----------------
def get_system_prompt(user_role="general"):
    instructions = (
        "FORMAT RULES:\n"
        "- Output must be plain text only.\n"
        "- Do NOT use asterisks (*), bold (**), hashtags (#), or any Markdown symbols.\n"
        "- Use only hyphens (-) or numbers for lists.\n"
        "- Separate sections and paragraphs with a blank line.\n"
        "- Answer ONLY what the user asks. Do not invent extra info.\n\n"
        "Example format:\n"
        "If user asks about admission:\n\n"
        "Admission Process\n\n"
        "Application Process:\n"
        "- Step 1...\n"
        "- Step 2...\n\n"
        "Testing Process:\n"
        "- Step 1...\n\n"
        "If user asks something else, answer directly in plain text with the same rules."
    )
    base = (
        "You are a helpful assistant for Padma Kanya College. "
        "Always give clean, organized plain text answers. "
        "Never use Markdown or formatting symbols. "
    )
    return base + instructions

# ---------------- QUERY OLLAMA ----------------
def query_ollama(prompt, model=OLLAMA_MODEL, user_role="general"):
    data = {
        "model": model,
        "prompt": prompt,
        "system": get_system_prompt(user_role),
        "stream": True
    }
    try:
        with requests.post(OLLAMA_URL, json=data, stream=True, timeout=60) as response:
            response.raise_for_status()
            result = ""
            for line in response.iter_lines(decode_unicode=True):
                if line:
                    try:
                        chunk = json.loads(line)
                        result += chunk.get("response", "")
                    except Exception as e:
                        print("Partial parse error:", e)
            return result if result else "Sorry, I couldn't process your request at the moment."
    except Exception as e:
        print(f"Ollama API error: {e}")
        return "Sorry, I couldn't process your request at the moment."

# ---------------- CLEAN RESPONSE ----------------
def clean_response(text):
    # Remove markdown (bold, italic, headings, etc.)
    text = re.sub(r'\*\*(.*?)\*\*', r'\1', text)   # **bold**
    text = re.sub(r'\*(.*?)\*', r'\1', text)       # *italic*
    text = re.sub(r'[`_>#]+', '', text)            # `, _, >, #

    # Force section titles on new lines
    sections = [
        "Admission Process",
        "Application Process",
        "Testing Process",
        "Personal Interview",
        "Selection and Offer Letter"
    ]
    for sec in sections:
        text = re.sub(rf'\s*{sec}', f'\n\n{sec}', text)

    # Normalize bullets
    text = re.sub(r'^\s*[\•]\s+', '- ', text, flags=re.MULTILINE)
    text = re.sub(r'^\s*\d+\.\s+', lambda m: m.group(0).replace('.', '') + ' ', text, flags=re.MULTILINE)
    text = re.sub(r'^\s*-\s+', '- ', text, flags=re.MULTILINE)

    # Clean paragraph spacing
    text = re.sub(r'\n{3,}', '\n\n', text)  # collapse 3+ newlines into 2
    text = re.sub(r'([^\n])\n([^\n])', r'\1\n\n\2', text)  # single → double

    return text.strip()

# ---------------- HANDLE USER QUERY ----------------
def handle_user_query(user_query):
    greetings = ["hi", "hello", "hey", "namaste"]
    if user_query.strip().lower() in greetings:
        return "Hello! How can I help you today?"
    
    # Otherwise call Ollama
    raw_response = query_ollama(user_query)
    return clean_response(raw_response)

# ---------------- MAIN ----------------
if __name__ == "__main__":
    while True:
        user_query = input("You: ")
        if user_query.lower() in ["quit", "exit"]:
            print("Bot: Goodbye!")
            break
        response = handle_user_query(user_query)
        print("Bot:", response)
