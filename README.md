# Music Downloader Bot (Advanced)

این نسخه‌ی پیشرفته از ربات تلگرام برای دریافت آهنگ از Apple Music است.

## امکانات:
- دریافت اطلاعات از لینک Apple Music
- جستجوی آهنگ در یوتیوب
- دریافت لینک دانلود مستقیم
- ارسال فایل MP3 در تلگرام

## مراحل اجرا در Render:

1. وارد [https://render.com](https://render.com) شو
2. روی New Web Service کلیک کن
3. این ریپو رو انتخاب کن
4. تنظیمات:
   - **Build Command:** `pip install -r requirements.txt`
   - **Start Command:** `python3 main.py`
   - **Env Var:** `BOT_TOKEN`

> توجه: آدرس API یوتیوب فیکه و باید جایگزین بشه با یه سرویس واقعی مثل yt-dlp سرور شخصی یا 3rd-party API.

سورس کد فقط جهت تست آموزشی آماده شده.