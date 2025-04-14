import requests
import time

# 🔐 Tokens
BOT_TOKEN = "8101200711:AAHJdTDfw53m0U_Cq5J9wTZZVlwvduD4eqk"
HF_TOKEN = "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"

# 🌐 URLs
TG_API = f"https://api.telegram.org/bot{BOT_TOKEN}"
GROQ_URL = "https://api-inference.huggingface.co/models/meta-llama/Meta-Llama-3-8B-Instruct"

def get_updates(offset=None):
    url = TG_API + "/getUpdates?timeout=100"
    if offset:
        url += f"&offset={offset}"
    return requests.get(url).json()

def send_message(chat_id, text):
    url = TG_API + "/sendMessage"
    requests.post(url, json={"chat_id": chat_id, "text": text})

def ask_groq(prompt):
    headers = {"Authorization": f"Bearer {HF_TOKEN}"}
    data = {"inputs": prompt}
    res = requests.post(GROQ_URL, headers=headers, json=data)
    try:
        return res.json()[0]["generated_text"]
    except:
        return "⚠️ Error from model."

def main():
    print("🤖 Bot running...")
    offset = None
    while True:
        updates = get_updates(offset)
        for update in updates.get("result", []):
            chat_id = update["message"]["chat"]["id"]
            text = update["message"].get("text")
            if text:
                print(f"User: {text}")
                reply = ask_groq(text)
                send_message(chat_id, reply)
            offset = update["update_id"] + 1
        time.sleep(1)

if __name__ == "__main__":
    main()
