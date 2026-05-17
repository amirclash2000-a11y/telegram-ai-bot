import os
import logging
import google.generativeai as genai
from telegram import Update
from telegram.ext import ApplicationBuilder, MessageHandler, filters, ContextTypes

logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

GEMINI_KEY = os.environ.get("GEMINI_API_KEY", "NOT_SET")
TELEGRAM_KEY = os.environ.get("TELEGRAM_TOKEN", "NOT_SET")

logger.info(f"GEMINI_API_KEY is {'SET' if GEMINI_KEY != 'NOT_SET' else 'NOT SET'}")
logger.info(f"TELEGRAM_TOKEN is {'SET' if TELEGRAM_KEY != 'NOT_SET' else 'NOT SET'}")

genai.configure(api_key=GEMINI_KEY)
model = genai.GenerativeModel("gemini-2.0-flash")

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    try:
        user_message = update.message.text
        logger.info(f"Received: {user_message}")
        response = model.generate_content(user_message)
        await update.message.reply_text(response.text)
    except Exception as e:
        logger.error(f"Error: {e}")
        await update.message.reply_text(f"خطا: {e}")

app = ApplicationBuilder().token(TELEGRAM_KEY).build()
app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))
app.run_polling()
