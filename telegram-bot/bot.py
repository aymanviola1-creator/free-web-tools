"""
Multi-Tool Telegram Bot with TON Donation Support
==================================================
Provides useful utilities and accepts TON/BTC/ETH tips.

Setup:
  1. pip install python-telegram-bot qrcode[pil] pyyaml
  2. Create a bot via @BotFather on Telegram, get the token
  3. Replace YOUR_BOT_TOKEN below
  4. python bot.py

Deploy for free:
  - Render.com (web service)
  - Railway.app
  - PythonAnywhere
"""

import os
import json
import logging
import io
import qrcode
import yaml

from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup, ParseMode
from telegram.ext import (
    Application, CommandHandler, MessageHandler,
    filters, CallbackQueryHandler, ContextTypes
)

# ============================================================
# CONFIGURATION - EDIT THESE
# ============================================================
BOT_TOKEN = os.environ.get("BOT_TOKEN", "YOUR_BOT_TOKEN_HERE")

# Your donation addresses (replace with your real wallets)
DONATION_ADDRESSES = {
    "TON": "UQDs9oGzBx4x7vV4sdfghjkl6d9e9fce5e9722125867babf48b084",  # Replace!
    "BTC": "bc1q6d9e9fce5e9722125867babf48b084",  # Replace!
    "ETH": "0x6d9e9fce5e9722125867babf48b084be1b0fcf28",  # Replace!
}

# ============================================================
# LOGGING
# ============================================================
logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    level=logging.INFO
)
logger = logging.getLogger(__name__)

# ============================================================
# COMMAND HANDLERS
# ============================================================

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Send a welcome message with available commands."""
    user = update.effective_user
    welcome_text = (
        f"👋 Hello {user.first_name}!\n\n"
        f"I'm a multi-tool bot. Here's what I can do:\n\n"
        f"🔧 **Utilities**\n"
        f"/qr `<text>` - Generate QR code\n"
        f"/json `<json>` - Format & validate JSON\n"
        f"/yaml `<yaml>` - Convert YAML to JSON\n"
        f"/base64 `<text>` - Base64 encode\n"
        f"/hash `<text>` - Generate SHA-256 hash\n"
        f"/uuid - Generate a UUID\n\n"
        f"💰 **Support**\n"
        f"/donate - Show donation addresses\n"
        f"/tip - How to send TON tips\n\n"
        f"📊 /stats - Bot usage statistics"
    )
    await update.message.reply_text(welcome_text, parse_mode=ParseMode.MARKDOWN)


async def donate_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Show donation addresses."""
    text = (
        "💰 **Support the developer**\n\n"
        "If you find this bot useful, please consider donating:\n\n"
    )
    for currency, address in DONATION_ADDRESSES.items():
        text += f"• **{currency}**: `{address}`\n\n"

    text += (
        "🤖 **Telegram TON Tip**:\n"
        "You can also send TON tips via @wallet or @tonRocketBot\n"
        "just type: `/tip @YourBotUsername 1 TON`\n\n"
        "Thank you for your support! 🙏"
    )

    keyboard = [
        [InlineKeyboardButton("⭐ Support on GitHub", url="https://github.com/aymanviola1-creator/free-web-tools")],
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)

    await update.message.reply_text(text, parse_mode=ParseMode.MARKDOWN, reply_markup=reply_markup)


async def qr_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Generate a QR code from text."""
    if not context.args:
        await update.message.reply_text("⚠️ Usage: /qr `<text>`\nExample: /qr https://example.com")
        return

    text = " ".join(context.args)

    try:
        img = qrcode.make(text)
        bio = io.BytesIO()
        bio.name = "qrcode.png"
        img.save(bio, "PNG")
        bio.seek(0)
        await update.message.reply_photo(photo=bio, caption=f"✅ QR Code for: {text[:50]}")
    except Exception as e:
        await update.message.reply_text(f"❌ Error generating QR: {str(e)}")


async def json_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Format and validate JSON."""
    if not context.args:
        await update.message.reply_text("⚠️ Usage: /json `<json_string>`\nExample: /json {\"name\":\"test\"}")
        return

    text = " ".join(context.args)

    try:
        parsed = json.loads(text)
        formatted = json.dumps(parsed, indent=2)
        await update.message.reply_text(f"✅ Valid JSON:\n```\n{formatted[:3900]}\n```", parse_mode=ParseMode.MARKDOWN)
    except json.JSONDecodeError as e:
        await update.message.reply_text(f"❌ Invalid JSON: {str(e)}")


async def yaml_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Convert YAML to JSON."""
    if not context.args:
        await update.message.reply_text("⚠️ Usage: /yaml `<yaml_string>`\nExample: /yaml key: value")
        return

    text = " ".join(context.args)

    try:
        parsed = yaml.safe_load(text)
        formatted = json.dumps(parsed, indent=2)
        await update.message.reply_text(f"✅ YAML → JSON:\n```\n{formatted[:3900]}\n```", parse_mode=ParseMode.MARKDOWN)
    except yaml.YAMLError as e:
        await update.message.reply_text(f"❌ Invalid YAML: {str(e)}")


async def base64_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Encode text to Base64."""
    import base64 as b64
    if not context.args:
        await update.message.reply_text("⚠️ Usage: /base64 `<text>`")
        return

    text = " ".join(context.args)
    encoded = b64.b64encode(text.encode()).decode()
    await update.message.reply_text(f"✅ Base64 encoded:\n`{encoded}`", parse_mode=ParseMode.MARKDOWN)


async def hash_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Generate SHA-256 hash."""
    import hashlib
    if not context.args:
        await update.message.reply_text("⚠️ Usage: /hash `<text>`")
        return

    text = " ".join(context.args)
    hash_obj = hashlib.sha256(text.encode())
    await update.message.reply_text(f"✅ SHA-256:\n`{hash_obj.hexdigest()}`", parse_mode=ParseMode.MARKDOWN)


async def uuid_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Generate a UUID."""
    import uuid
    uid = str(uuid.uuid4())
    await update.message.reply_text(f"✅ UUID v4:\n`{uid}`", parse_mode=ParseMode.MARKDOWN)


async def stats_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Show simple stats."""
    await update.message.reply_text(
        "📊 **Bot Stats**\n\n"
        "• Commands available: 10\n"
        "• QR, JSON, YAML, Base64, Hash, UUID\n"
        "• TON/BTC/ETH donation support\n"
        "• Free & open source\n\n"
        "⭐ Star on GitHub to support!",
        parse_mode=ParseMode.MARKDOWN
    )


async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Show help."""
    await start(update, context)


async def error_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Log errors."""
    logger.error(f"Update {update} caused error {context.error}")


def main():
    """Start the bot."""
    if BOT_TOKEN == "YOUR_BOT_TOKEN_HERE":
        print("=" * 60)
        print("  ERROR: You need to set your bot token!")
        print("=" * 60)
        print()
        print("  1. Open Telegram, search for @BotFather")
        print("  2. Send /newbot and follow instructions")
        print("  3. Copy the token")
        print("  4. Set it as environment variable:")
        print("     Windows: set BOT_TOKEN=your_token_here")
        print("     Linux/Mac: export BOT_TOKEN=your_token_here")
        print("  5. Or edit bot.py and replace YOUR_BOT_TOKEN_HERE")
        print()
        return

    # Create application
    application = Application.builder().token(BOT_TOKEN).build()

    # Register handlers
    application.add_handler(CommandHandler("start", start))
    application.add_handler(CommandHandler("help", help_command))
    application.add_handler(CommandHandler("donate", donate_command))
    application.add_handler(CommandHandler("qr", qr_command))
    application.add_handler(CommandHandler("json", json_command))
    application.add_handler(CommandHandler("yaml", yaml_command))
    application.add_handler(CommandHandler("base64", base64_command))
    application.add_handler(CommandHandler("hash", hash_command))
    application.add_handler(CommandHandler("uuid", uuid_command))
    application.add_handler(CommandHandler("stats", stats_command))

    # Error handler
    application.add_error_handler(error_handler)

    # Start polling
    print("🤖 Bot is running... Press Ctrl+C to stop.")
    application.run_polling(allowed_updates=Update.ALL_TYPES)


if __name__ == "__main__":
    main()
