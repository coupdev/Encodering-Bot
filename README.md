# 🔒Encodering-Bot

[![Author](https://img.shields.io/badge/Author-@coupdev-blue)](https://coupdev.com)
[![License](https://img.shields.io/badge/License-MIT-blue)](#license)

---

## 🛡️ Overview

Encodering-Bot is a Telegram bot built with Python and [aiogram](https://docs.aiogram.dev/en/latest/) that allows users to encode and decode messages using Base64. Additionally, it supports sending encrypted messages only readable by a specified user, with multi-language support (English and Russian).

---

## 🚀 Features

- Base64 encode/decode commands: /encode, /decode
- Send private encrypted messages using /sendto @username <text>
- Access control: only the intended recipient can decrypt messages
- Multilingual interface with English 🇬🇧 and Russian 🇷🇺
- Secure message handling without storing plaintext messages permanently
- Easy to configure and deploy

---

## 📦 Requirements

- Python 3.11+
- aiogram library
- python-dotenv for environment variable management

---

## ⚙️ Setup & Installation

1. Clone the repository:

   ```bash
   git clone https://github.com/coupdev/Encodering-Bot.git
   cd Encodering-Bot
   ```

2. Create and activate a Python virtual environment:
   ```bash
   python -m venv venv
   source venv/bin/activate      # Linux/MacOS
   venv\Scripts\activate.bat     # Windows
   ```

3. Install dependencies:

   ```bash
   pip install -r requirements.txt
   ```

4. Create .env file:
Copy .env.example and fill in your bot token from @BotFather: (https://t.me/BotFather)

  ```bash
  BOT_TOKEN=your_token_bot
  ```

5. [Optional] Create access.json for permission management:
Use access.json.example as a template.

---

## 🚀 Running the Bot
Start the bot with:

```bash
python main.py
```

You should see:

```bash
Bot is running...
```

---

## 🤖 Usage
- /start — Welcome message with commands list
- /help — Help with commands
- /encode <text> — Encode text to Base64
- /decode <base64> — Decode Base64 text (if allowed)
- /sendto @username <text> — Send encrypted message readable only by that user
- Language selection inline buttons (English / Russian)

---

## 🔒 Access Control

The bot stores allowed user IDs for each encoded message in access.json. Only users in the allowed list can decrypt those messages.

Message content is stored only in Base64 format; plaintext is never saved.

---

## 🌐 Localization

Supports English and Russian out-of-the-box. The language is automatically detected based on the user’s Telegram language or can be changed with inline buttons.

---

## 🤝 Contributing

Feel free to open issues or pull requests. Suggestions for new languages, features, or improvements are welcome

---
