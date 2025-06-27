# 🤖 Aira — Telegram AI Assistant Bot

Aira is a focused Telegram bot built using Telethon and OpenRouter. It acts as a polite and intelligent assistant that handles messages on your behalf and summarizes conversations for follow-up.

## 🔧 Features
- Auto replies to Telegram DMs using OpenRouter (ChatGPT-style API)
- Summarizes user intent and logs to a text file
- Inactivity detection with auto-session cleanup
- Designed for minimal, focused conversations

## 🚀 Deploy on Render

1. Clone the repo
2. Add `.env` file (see `.env.example`)
3. Add secrets via Render Dashboard
4. Deploy and you're done!

## 📁 Project Structure
- `main.py`: The bot logic
- `.env.example`: Sample environment variables
- `aira_summaries.txt`: Saved session summaries
- `requirements.txt`: Python dependencies

## 🔐 Note
**Never commit your `.env` or session files!** Use `.gitignore` properly.
