import os
from telegram import Update, InputFile
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, filters, ContextTypes

TOKEN = os.getenv("BOT_TOKEN") or "YOUR_BOT_TOKEN_HERE"

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("سلام! لینک آهنگتو بفرست تا دانلود کنم.")

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = update.message.text
    if "music.apple.com" in text:
        await update.message.reply_text("در حال پردازش لینک... (اینجا می‌تونه آهنگ واقعی دریافت بشه)")
        # جای دانلود و ارسال فایل واقعی
        await update.message.reply_audio(audio=InputFile("sample.mp3"), caption="این یه نمونه‌ست.")
    else:
        await update.message.reply_text("لطفاً لینک معتبر اپل موزیک بفرست.")

if __name__ == "__main__":
    app = ApplicationBuilder().token(TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))
    app.run_polling()