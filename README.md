# Hashashin Control Panel

یک اپلیکیشن Kivy برای کنترل و نظارت بر سیستم

## ویژگی‌ها

- نمایش اطلاعات سیستم
- نظارت بر پردازش‌ها
- بررسی سرویس‌ها
- اطلاعات شبکه
- فضای دیسک
- کاربران محلی
- استفاده از CPU و حافظه
- ارسال اطلاعات به تلگرام

## نصب و اجرا

### Windows:
```bash
# فعال کردن virtual environment
Scripts\activate.bat

# نصب dependencies
pip install -r requirements.txt

# اجرای اپلیکیشن
python main.py
```

### Android (با GitHub Actions):
1. پروژه رو به GitHub push کنید
2. به Actions tab بروید
3. APK رو از Artifacts دانلود کنید

### Android (محلی):
```bash
# نصب Buildozer
pip install buildozer

# ساخت APK
buildozer android debug
```

## تنظیمات تلگرام

برای استفاده از قابلیت ارسال به تلگرام، token و chat_id رو در فایل `hashashin_kivy.py` تغییر بدید.

## فایل‌های پروژه

- `main.py` - Entry point اپلیکیشن
- `hashashin_kivy.py` - کد اصلی اپلیکیشن
- `buildozer.spec` - تنظیمات Android
- `requirements.txt` - Dependencies پایتون
- `.github/workflows/build-android.yml` - GitHub Actions برای ساخت APK

## مجوزها

این پروژه تحت مجوز MIT منتشر شده است.

