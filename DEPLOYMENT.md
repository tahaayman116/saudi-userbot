# 🚀 دليل النشر على Railway (مجاني)

## المتطلبات

- حساب GitHub
- حساب Railway (مجاني)
- توكن البوت من BotFather
- معرف المستخدم الخاص بك

## خطوات النشر

### 1. إنشاء مستودع GitHub

```bash
# في مجلد المشروع
git init
git add .
git commit -m "Initial Saudi Bot commit"

# إنشاء مستودع جديد على GitHub ثم:
git remote add origin https://github.com/username/saudi-telegram-bot.git
git branch -M main
git push -u origin main
```

### 2. إنشاء مشروع Railway

1. اذهب إلى [railway.app](https://railway.app)
2. انقر "Login" واختر GitHub
3. انقر "New Project"
4. اختر "Deploy from GitHub repo"
5. اختر المستودع الذي أنشأته

### 3. إعداد متغيرات البيئة

في لوحة تحكم Railway:

1. انقر على المشروع
2. اذهب إلى تبويب "Variables"
3. أضف المتغيرات التالية:

```
TELEGRAM_BOT_TOKEN=1234567890:ABCdefGHIjklMNOpqrsTUVwxyz
OWNER_ID=123456789
```

### 4. تفعيل الـ Webhook

بعد نشر المشروع:

1. انسخ رابط المشروع من Railway (مثل: `https://saudi-bot-production.up.railway.app`)
2. افتح المتصفح واذهب إلى:

```
https://api.telegram.org/bot<YOUR_BOT_TOKEN>/setWebhook?url=<YOUR_RAILWAY_URL>/<YOUR_BOT_TOKEN>
```

مثال:
```
https://api.telegram.org/bot1234567890:ABCdefGHIjklMNOpqrsTUVwxyz/setWebhook?url=https://saudi-bot-production.up.railway.app/1234567890:ABCdefGHIjklMNOpqrsTUVwxyz
```

### 5. اختبار البوت

1. ابحث عن البوت في تلجرام
2. أرسل `/start`
3. يجب أن يرد عليك البوت

## إعدادات Railway المتقدمة

### تخصيص النطاق

1. في لوحة تحكم Railway
2. اذهب إلى "Settings"
3. في قسم "Domains" يمكنك إضافة نطاق مخصص

### مراقبة الأداء

1. تبويب "Metrics" يعرض استخدام الموارد
2. تبويب "Logs" يعرض سجلات البوت

### إعادة النشر

```bash
# عند تعديل الكود
git add .
git commit -m "Update bot"
git push

# Railway سيعيد النشر تلقائياً
```

## استكشاف الأخطاء

### البوت لا يعمل

1. تحقق من السجلات في Railway
2. تأكد من متغيرات البيئة
3. تأكد من تفعيل الـ Webhook

### خطأ في الـ Webhook

```bash
# لحذف الـ Webhook
curl "https://api.telegram.org/bot<YOUR_BOT_TOKEN>/deleteWebhook"

# لإعادة تعيينه
curl "https://api.telegram.org/bot<YOUR_BOT_TOKEN>/setWebhook?url=<YOUR_RAILWAY_URL>/<YOUR_BOT_TOKEN>"
```

### مشكلة في النشر

1. تأكد من وجود `Procfile`
2. تأكد من وجود `requirements.txt`
3. تأكد من `runtime.txt` (اختياري)

## الحدود المجانية لـ Railway

- 500 ساعة تشغيل شهرياً
- 1GB RAM
- 1GB تخزين
- مناسب للبوتات الصغيرة والمتوسطة

## نصائح للتوفير

1. استخدم النسخة المبسطة (`railway_bot.py`)
2. قلل من عدد المجموعات المراقبة
3. راقب استخدام الموارد

## بدائل مجانية أخرى

- **Heroku** (محدود)
- **Render** (750 ساعة مجانية)
- **Fly.io** (محدود)
- **PythonAnywhere** (محدود)

---

**ملاحظة:** تأكد من الالتزام بشروط الاستخدام لكل منصة.
