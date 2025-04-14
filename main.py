import os
import re
import requests
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, filters, ContextTypes

TOKEN = os.getenv("BOT_TOKEN")

APPLE_REGEX = r"(https?://music\.apple\.com[^\s]+)"

def extract_apple_music_info(url):
    try:
        response = requests.get(url)
        if response.ok:
            title_match = re.search(r'<title>(.*?)</title>', response.text)
            image_match = re.search(r'(https://is[^"]+\.jpg)', response.text)
            if title_match:
                title_parts = title_match.group(1).split(' - ')
                track = title_parts[0].strip()
                artist = title_parts[1].strip() if len(title_parts) > 1 else ''
                image_url = image_match.group(1) if image_match else None
                return track, artist, image_url
    except:
        pass
    return None, None, None

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("سلام! لینک Apple Music رو بفرست تا اطلاعاتش رو برات بیارم.")

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = update.message.text.strip()
    match = re.search(APPLE_REGEX, text)
    if not match:
        await update.message.reply_text("لطفاً یک لینک معتبر Apple Music بفرست.")
        return

    url = match.group(1)
    await update.message.reply_text("در حال پردازش لینک...")

    track, artist, image_url = extract_apple_music_info(url)
    if not track:
        await update.message.reply_text("اطلاعاتی از این لینک پیدا نشد.")
        return

    caption = f"*{track}*\nby _{artist}_" if artist else f"*{track}*"
    if image_url:
        await update.message.reply_photo(photo=image_url, caption=caption, parse_mode="Markdown")
    else:
        await update.message.reply_text(caption, parse_mode="Markdown")

if __name__ == "__main__":
    app = ApplicationBuilder().token(TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))
    app.run_polling()