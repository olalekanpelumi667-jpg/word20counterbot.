# Word Counter Bot (@word20counterbot)

A simple Telegram bot that counts words, characters, sentences, and lines in any text you send it.

## Features
- `/start` — welcome message
- `/help` — list of commands
- `/count <text>` — analyze specific text
- Send any plain message — it's analyzed automatically

---

## 1. Create the bot on Telegram (BotFather)

1. Open Telegram and search for **@BotFather**.
2. Send `/newbot`.
3. Choose a display name (e.g. `Word Counter`).
4. Choose the username: `word20counterbot` (must end in "bot").
5. BotFather will give you a **token** — looks like `123456789:ABCdefGhIJKlmNoPQRstuVwxYZ`. Copy it, you'll need it soon.

Optional polish:
- `/setdescription` — short description shown before someone starts a chat.
- `/setabouttext` — shown on the bot's profile.
- `/setuserpic` — upload a profile picture.
- `/setcommands` — paste this so Telegram shows a command menu:
  ```
  start - Welcome message
  help - Show help
  count - Count words in given text
  ```

---

## 2. Push this project to GitHub

From this folder:

```bash
git init
git add .
git commit -m "Initial commit: word counter bot"
git branch -M main
git remote add origin https://github.com/<your-username>/word20counterbot.git
git push -u origin main
```

(Create the empty repo first on github.com, or use `gh repo create` if you have the GitHub CLI.)

**Important:** Never commit your bot token. It's read from an environment variable, and `.env` is already excluded via `.gitignore`.

---

## 3. Deploy on Railway

1. Go to [railway.app](https://railway.app) and log in (GitHub login works well here).
2. Click **New Project → Deploy from GitHub repo**.
3. Select your `word20counterbot` repository.
4. Railway will detect `requirements.txt` and `Procfile` automatically and treat this as a **worker** (background process), not a web service — no need to expose a port since this bot uses polling.
5. Go to the project's **Variables** tab and add:
   - `BOT_TOKEN` = the token you got from BotFather.
6. Deploy. Check the **Deployments → Logs** tab — you should see:
   ```
   Bot started. Polling for updates...
   ```
7. Open Telegram, search `@word20counterbot`, and send `/start`.

---

## 4. Local testing (optional, before deploying)

```bash
python -m venv venv
source venv/bin/activate      # Windows: venv\Scripts\activate
pip install -r requirements.txt
export BOT_TOKEN="your-token-here"   # Windows: set BOT_TOKEN=your-token-here
python bot.py
```

---

## File structure

```
word20counterbot/
├── bot.py             # main bot logic
├── requirements.txt   # dependencies
├── Procfile           # tells Railway how to run the bot
├── runtime.txt         # Python version pin
├── .gitignore
└── README.md
```

## Notes
- This bot uses **polling**, which is the simplest way to run on Railway — no webhook/domain setup needed.
- If you later want faster response times at scale, you can switch to a webhook-based setup, but polling is perfectly fine for personal/small projects.
