import os
import re
import requests
from telegram import Update, InputMediaAudio
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, filters, ContextTypes

TOKEN = os.getenv("BOT_TOKEN")

APPLE_REGEX = r"(https?://music\.apple\.com[^\s]+)"

YOUTUBE_API_URL = "https://yt-api-fake.example.com/convert?q={}"  # نمونه فرضی

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("سلام! لینک اپل موزیک آهنگت رو بفرست تا برات دانلودش کنم.")

def extract_apple_music_info(url):
    try:
        response = requests.get(url)
        if response.ok:
            # ساده‌شده: تایتل آهنگ رو از متای اپل موزیک می‌گیریم
            title_match = re.search(r'<title>(.*?)</title>', response.text)
            if title_match:
                title = title_match.group(1).split(' - ')[0]
                artist = title_match.group(1).split(' - ')[1] if ' - ' in title_match.group(1) else ""
                return title.strip(), artist.strip()
    except:
        return None, None
    return None, None

def search_youtube_download_link(title, artist):
    # شبیه‌سازی فراخوانی به API تبدیل یوتیوب
    query = f"{title} {artist}".strip().replace(" ", "+")
    # فرض می‌کنیم این API لینک مستقیم می‌ده
    response = requests.get(YOUTUBE_API_URL.format(query))
    if response.ok:
        data = response.json()
        return data.get("download_url", None)
    return None

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = update.message.text.strip()
    match = re.search(APPLE_REGEX, text)
    if not match:
        await update.message.reply_text("لطفاً فقط لینک معتبر Apple Music بفرست.")
        return

    url = match.group(1)
    await update.message.reply_text("در حال دریافت اطلاعات آهنگ...")

    title, artist = extract_apple_music_info(url)
    if not title:
        await update.message.reply_text("نتونستم اطلاعاتی از این لینک استخراج کنم.")
        return

    audio_url = search_youtube_download_link(title, artist)
    if not audio_url:
        await update.message.reply_text("آهنگ پیدا نشد یا مشکلی در تبدیل پیش اومد.")
        return

    caption = f"**{title}**
by *{artist}*

درخواست‌شده توسط: {update.effective_user.first_name}"
    await update.message.reply_audio(audio=audio_url, caption=caption, parse_mode="Markdown")

if __name__ == "__main__":
    app = ApplicationBuilder().token(TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))
    app.run_polling()