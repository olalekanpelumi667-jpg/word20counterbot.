import os
import logging
import re

from telegram import Update
from telegram.ext import (
    ApplicationBuilder,
    CommandHandler,
    MessageHandler,
    ContextTypes,
    filters,
)

# ---------- Logging ----------
logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    level=logging.INFO,
)
logger = logging.getLogger(__name__)

# ---------- Bot token ----------
# Set this as an environment variable on Railway (BOT_TOKEN), never hardcode it.
BOT_TOKEN = os.environ.get("BOT_TOKEN")


def analyze_text(text: str) -> dict:
    """Return word/character/sentence/line stats for a given text."""
    words = text.split()
    word_count = len(words)
    char_count_with_spaces = len(text)
    char_count_no_spaces = len(text.replace(" ", "").replace("\n", ""))
    sentence_count = len(re.findall(r"[.!?]+", text)) or (1 if text.strip() else 0)
    line_count = len(text.splitlines()) or (1 if text.strip() else 0)
    avg_word_len = (
        round(sum(len(w) for w in words) / word_count, 2) if word_count else 0
    )

    return {
        "words": word_count,
        "chars_with_spaces": char_count_with_spaces,
        "chars_no_spaces": char_count_no_spaces,
        "sentences": sentence_count,
        "lines": line_count,
        "avg_word_len": avg_word_len,
    }


# ---------- Handlers ----------
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    msg = (
        "👋 Hi! I'm *Word Counter Bot*.\n\n"
        "Just send me any text and I'll count:\n"
        "• Words\n"
        "• Characters (with & without spaces)\n"
        "• Sentences\n"
        "• Lines\n"
        "• Average word length\n\n"
        "Type /help to see all commands."
    )
    await update.message.reply_text(msg, parse_mode="Markdown")


async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    msg = (
        "*Available commands:*\n"
        "/start - Welcome message\n"
        "/help - Show this help message\n"
        "/count <text> - Count stats for the given text\n\n"
        "You can also just send plain text directly (no command needed) "
        "and I'll analyze it automatically."
    )
    await update.message.reply_text(msg, parse_mode="Markdown")


async def count_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = " ".join(context.args)
    if not text:
        await update.message.reply_text(
            "Please provide some text.\nExample: `/count Hello world!`",
            parse_mode="Markdown",
        )
        return
    await send_stats(update, text)


async def handle_text(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = update.message.text
    if text:
        await send_stats(update, text)


async def send_stats(update: Update, text: str):
    stats = analyze_text(text)
    reply = (
        "📊 *Text Stats*\n\n"
        f"📝 Words: `{stats['words']}`\n"
        f"🔤 Characters (with spaces): `{stats['chars_with_spaces']}`\n"
        f"🔡 Characters (no spaces): `{stats['chars_no_spaces']}`\n"
        f"📖 Sentences: `{stats['sentences']}`\n"
        f"📄 Lines: `{stats['lines']}`\n"
        f"📏 Avg. word length: `{stats['avg_word_len']}`"
    )
    await update.message.reply_text(reply, parse_mode="Markdown")


async def error_handler(update: object, context: ContextTypes.DEFAULT_TYPE):
    logger.error("Update %s caused error %s", update, context.error)


def main():
    if not BOT_TOKEN:
        raise RuntimeError(
            "BOT_TOKEN environment variable is not set. "
            "Set it in Railway's Variables tab."
        )

    app = ApplicationBuilder().token(BOT_TOKEN).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("help", help_command))
    app.add_handler(CommandHandler("count", count_command))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_text))
    app.add_error_handler(error_handler)

    logger.info("Bot started. Polling for updates...")
    app.run_polling(allowed_updates=Update.ALL_TYPES)


if __name__ == "__main__":
    main()
