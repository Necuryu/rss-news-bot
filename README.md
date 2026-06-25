# 📰 RSS News Monitor Bot

A Telegram bot that monitors news sources and instantly delivers articles matching your keywords. Supports 🇷🇺 Russian and 🇬🇧 English.

## Features

- 🔍 Keyword-based filtering — get only news you care about
- 📡 Custom RSS sources — add any news site
- ⭐ Popular sources built-in (BBC, CoinDesk, TechCrunch, Reuters)
- 🔔 Real-time monitoring — checks every 5 minutes
- 🌐 Bilingual interface (RU / EN)
- 💬 Fully button-driven — no commands needed

## How It Works

1. Start the bot with `/start`
2. Choose your language
3. Add news sources (RSS feeds)
4. Add keywords to filter
5. Press ▶️ Start — receive matching articles automatically

## Setup

1. Clone the repository
2. Install dependencies:



3. Replace `YOUR_BOT_TOKEN_HERE` in `rss_bot.py` with your token from [@BotFather](https://t.me/BotFather)
4. Run:

## Built With

- Python 3
- pyTelegramBotAPI
- feedparser
- RSS feeds (no API key required)
