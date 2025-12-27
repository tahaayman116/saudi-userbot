# استخدام Python 3.11 slim image
FROM python:3.11-slim

# تعيين مجلد العمل
WORKDIR /app

# نسخ ملفات المتطلبات
COPY requirements.txt requirements_cloud.txt requirements_userbot.txt ./

# تثبيت المكتبات المطلوبة
RUN pip install --no-cache-dir -r requirements_userbot.txt && \
    pip install --no-cache-dir telethon cryptg aiofiles

# نسخ جميع ملفات المشروع
COPY . .

# تعيين متغيرات البيئة الافتراضية
ENV PYTHONUNBUFFERED=1

# الأمر الافتراضي لتشغيل البوت
CMD ["python", "cloud_userbot.py"]
