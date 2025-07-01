# 🤖 Aira — Telegram AI Assistant Bot

Aira is a focused Telegram bot built using Telethon and OpenRouter. It acts as a polite and intelligent assistant that handles messages on your behalf and summarizes conversations for follow-up.

---

## 🔧 Features
- Auto replies to Telegram DMs using OpenRouter (ChatGPT-style API)
- Summarizes user intent and logs to a text file
- Inactivity detection with auto-session cleanup
- Designed for minimal, focused conversations
- Flask web server for uptime monitoring (Render keep-alive)

---

## 🚀 Deployment Options

### 🔹 Option 1: Run Locally (Recommended for development)

1. **Clone the repository**  
   ```bash
   git clone https://github.com/yourusername/aira.git
   cd aira

2. Create and activate a virtual environment

```bash
python -m venv venv
source venv/bin/activate  # on Windows: venv\Scripts\activate
```

3. Install dependencies
```bash
pip install -r requirements.txt
```

4. Set up environment variables
Rename .env.example to .env

Fill in your:
API_ID
API_HASH
OPENROUTER_API_KEY
OWNER_ID
(Optional but preferred) SESSION_STRING (see below)


5. (Optional) Generate a String Session
If you don’t want to use .session files, generate a session string:

```bash
python generate_session.py
```

Paste the output into your .env under SESSION_STRING.


6. Start the bot
```bash
python main.py
```
---

### 🔹 Option 2: Deploy on Render (Userbot via Worker Service)

> Telethon userbots need to run as long-lived background processes. This works best using a Worker service on Render.

1. Clone the repo to your GitHub
2. Set up a Worker service on Render:
Use render.yaml as the deploy spec
3. Add your environment variables via the Render Dashboard
4. Deploy the service
⚠️ Note: You must generate a SESSION_STRING locally and add it as an environment variable. Render cannot do interactive logins for userbots.


---

📁 Project Structure

File	Description

main.py	Main bot logic
generate_session.py	Tool to generate a session string
.env.example	Sample env file for local dev
aira_summaries.txt	Conversation summary logs
requirements.txt	Python dependencies
render.yaml	Deployment config for Render Worker

---

🛡️ Security Notes

Never commit your .env or .session files
Use .gitignore to prevent secrets from being pushed
Use a string session instead of session files for safer deployments

---

📞 Contact

### Want to customize or extend Aira? Reach out or fork this repo — and remember to stay polite like Aira 😉
---

