# Multi-Tool Telegram Bot

A Telegram bot with useful utilities (QR code, JSON/YAML formatting, hashing, etc.)
that accepts TON/BTC/ETH tips for monetization.

## Features

- /qr `<text>` - Generate QR codes
- /json `<json>` - Format and validate JSON
- /yaml `<yaml>` - Convert YAML to JSON
- /base64 `<text>` - Base64 encode
- /hash `<text>` - SHA-256 hash generator
- /uuid - Generate UUID v4
- /donate - Show donation addresses (TON, BTC, ETH)
- /stats - Bot statistics
- /start - Welcome message

## Quick Start

1. Create a bot via [@BotFather](https://t.me/BotFather) on Telegram
2. Copy the token
3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
4. Set your token:
   ```bash
   export BOT_TOKEN=your_token_here
   ```
5. Run the bot:
   ```bash
   python bot.py
   ```

## Deploy for Free

### Render.com
1. Push to GitHub
2. Create a new Web Service on Render
3. Set start command: `python bot.py`
4. Add `BOT_TOKEN` as environment variable
5. Deploy!

### Railway.app
1. Push to GitHub
2. Create new project from repo
3. Add `BOT_TOKEN` as environment variable
4. Deploy!

## Monetization

The bot displays donation addresses for:
- **TON** (Telegram Open Network) - native Telegram crypto
- **Bitcoin (BTC)**
- **Ethereum (ETH)**

Users can also send TON tips via @wallet or @tonRocketBot.

## License

MIT
