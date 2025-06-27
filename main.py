from telethon import TelegramClient, events
import requests
import asyncio
from collections import defaultdict
import time



# 🔑 API credentials
import os
from dotenv import load_dotenv
load_dotenv()

api_id = int(os.getenv("API_ID"))
api_hash = os.getenv("API_HASH")
OPENROUTER_API_KEY = os.getenv("OPENROUTER_API_KEY")
OWNER_ID = int(os.getenv("OWNER_ID"))

required_vars = [api_id, api_hash, OPENROUTER_API_KEY, OWNER_ID]
if not all(required_vars):
    raise EnvironmentError("❌ Missing one or more required environment variables in .env file.")

MODEL = "deepseek/deepseek-chat-v3-0324"


# 🕒 Timeout for inactivity (seconds)
INACTIVITY_TIMEOUT = 60

# 👥 Track sessions
conversation_history = defaultdict(list)
last_message_time = {}
inactivity_tasks = {}
session_complete = {}

# 🧠 Ask OpenRouter
def ask_openrouter(prompt: str, history=None) -> str:
    url = "https://openrouter.ai/api/v1/chat/completions"
    headers = {
        "Authorization": f"Bearer {OPENROUTER_API_KEY}",
        "Content-Type": "application/json",
        "HTTP-Referer": "https://yourdomain.com",
        "X-Title": "Aira-Telegram",
    }

    messages = [
        {
            "role": "system",
            "content": (
                "You are Aira, an intelligent, respectful AI assistant representing your Owner. "
                "Your sole job is to ask the user why they are trying to contact the Owner, what the meeting or message is about, and gather key details if needed. "
                "You should not provide general assistance, answer unrelated questions, or engage in casual chat. "
                "Keep your replies short, polite, and strictly focused on understanding the purpose. "
                "Inform the user that Owner will be available soon. "
                "Once the reason is clear, acknowledge it, confirm you’ll pass it to the Owner, and politely end the conversation. "
                "On the first message, you should introduce yourself briefly as Aira, A Personal A.I. Assistant, and ask the user for the purpose of their message."
            )
        }
    ]

    if history:
        messages += history
    else:
        messages.append({"role": "user", "content": prompt})

    body = {
        "model": MODEL,
        "messages": messages
    }

    response = requests.post(url, headers=headers, json=body)
    if response.status_code == 200:
        return response.json()["choices"][0]["message"]["content"]
    else:
        print(f"❌ OpenRouter API error {response.status_code}: {response.text}")
        return "⚠️ Sorry, I couldn’t process your message right now. Please try again shortly."


# 🚀 Start client
client = TelegramClient("aira_session", api_id, api_hash)

async def send_session_summary(user_id, sender):
    await asyncio.sleep(INACTIVITY_TIMEOUT)

    if time.time() - last_message_time.get(user_id, 0) >= INACTIVITY_TIMEOUT:
        history = conversation_history.get(user_id, [])
        if not history:
            return

        # Convert chat into readable form
        chat_lines = []
        for msg in history:
            role = "User" if msg["role"] == "user" else "Aira"
            chat_lines.append(f"{role}: {msg['content']}")

        joined = "\n".join(chat_lines)

        # Full summary for Telegram
        full_prompt = (
            f"This is a chat between Aira (AI assistant) and a user. "
            f"Summarize the user's intent and any instructions or details provided:\n\n{joined}"
        )
        full_summary = ask_openrouter(full_prompt)

        summary = (
            f"📬 Summary from {sender.first_name} (@{sender.username or 'no_username'}):\n\n"
            f"{full_summary}\n\n✅ Session ended due to inactivity."
        )
        await client.send_message(OWNER_ID, summary)

        # One-line short summary for text file
        short_prompt = (
            f"Summarize this conversation in one line, like: 'New message from Alex about meeting schedule':\n\n{joined}"
        )
        short_summary = ask_openrouter(short_prompt).strip()

        with open("aira_summaries.txt", "a", encoding="utf-8") as f:
            f.write(short_summary + "\n")

        # Clean up
        conversation_history.pop(user_id, None)
        last_message_time.pop(user_id, None)
        inactivity_tasks.pop(user_id, None)
        session_complete.pop(user_id, None)

@client.on(events.NewMessage)
async def handler(event):
    if event.out:
        return

    sender = await event.get_sender()
    if not event.is_private or getattr(sender, "bot", False):
        return

    try:
        await event.mark_read()
        user_id = sender.id
        msg = event.text.strip()

        print(f"📩 Message from {sender.first_name}: {msg}")

        # Even if session is done, update timestamp to avoid summary flood
        if session_complete.get(user_id):
            last_message_time[user_id] = time.time()
            return

        # Append to history
        history = conversation_history[user_id]
        history.append({"role": "user", "content": msg})

        # ⏩ Trim history to last 10 exchanges (20 messages max)
        if len(history) > 10:
            history = history[-10:]
            conversation_history[user_id] = history

        # Ask AI
        response = ask_openrouter(prompt=msg, history=history)
        await event.reply(response)

        # Save AI reply
        history.append({"role": "assistant", "content": response})
        last_message_time[user_id] = time.time()

        # Auto-close session
        if any(
            x in response.lower()
            for x in [
                "i’ll pass this to owner",
                "i’ll make sure owner sees this",
                "i’ll let the owner know"
            ]
        ):
            session_complete[user_id] = True

        # Reset inactivity timer
        if user_id in inactivity_tasks:
            inactivity_tasks[user_id].cancel()
        inactivity_tasks[user_id] = asyncio.create_task(send_session_summary(user_id, sender))

    except Exception as e:
        print("⚠️ Error in handler:", e)

# 🔧 Run
if __name__ == "__main__":
    print("🤖 Aira is now running...")
    client.start()
    client.run_until_disconnected()