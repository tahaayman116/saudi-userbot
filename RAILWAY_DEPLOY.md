# 🚀 نشر سريع على Railway - خطوة بخطوة

## الخطوة 1: إعداد Session String

```bash
pip install telethon
python quick_deploy.py
```

سيطلب منك:
- API ID و API Hash (من my.telegram.org)
- رمز التحقق من تلجرام

**النتيجة:** ملف `DEPLOY_VARS.txt` يحتوي على جميع المتغيرات المطلوبة

## الخطوة 2: رفع الكود على GitHub

```bash
# أنشئ مستودع جديد على GitHub أولاً
# ثم شغل هذه الأوامر:

git init
git add .
git commit -m "Saudi User Bot - Ready for Railway"
git branch -M main
git remote add origin https://github.com/YOUR_USERNAME/saudi-userbot.git
git push -u origin main
```

## الخطوة 3: النشر على Railway

### أ. إنشاء المشروع
1. اذهب إلى [railway.app](https://railway.app)
2. انقر "Login" → اختر GitHub
3. انقر "New Project"
4. اختر "Deploy from GitHub repo"
5. اختر المستودع الذي رفعته

### ب. إضافة متغيرات البيئة
1. في لوحة تحكم Railway
2. انقر على المشروع
3. اذهب إلى تبويب "Variables"
4. أضف المتغيرات من ملف `DEPLOY_VARS.txt`:

```
TELEGRAM_API_ID=123456789
TELEGRAM_API_HASH=abcdef123456789abcdef
TELEGRAM_SESSION_STRING=النص_الطويل_من_الملف
KEYWORDS=يسوي,يحل,يساعدني,ابي شخص,تعرفون حد,ابي حد,محتاج,اريد,اطلب,ممكن حد
```

### ج. إعداد Worker
1. اذهب إلى "Settings"
2. في قسم "Deploy"
3. تأكد من:
   - **Start Command:** `python cloud_userbot.py`
   - **Build Command:** `pip install -r requirements_cloud.txt`

### د. تفعيل النشر
1. انقر "Deploy"
2. انتظر انتهاء البناء (2-3 دقائق)
3. تحقق من "Logs" للتأكد من عدم وجود أخطاء

## الخطوة 4: التأكد من العمل

### في Railway Logs يجب أن ترى:
```
Started as [اسمك] (ID: 123456789)
Cloud User bot is running...
```

### في تلجرام (Saved Messages):
```
🤖 بوت المراقبة السحابي بدأ العمل!

📊 الإحصائيات:
🔑 الكلمات المفتاحية: 14
☁️ يعمل على الخادم السحابي

✅ البوت جاهز لمراقبة المجموعات!
```

## 🔧 استكشاف الأخطاء

### البوت لا يبدأ:
```bash
# في Railway، اذهب إلى Logs وابحث عن:
railway logs --tail
```

**الأخطاء الشائعة:**
- `Missing TELEGRAM_SESSION_STRING` → تأكد من إضافة Session String
- `API ID must be a number` → تأكد من API ID رقم صحيح
- `Invalid session` → أعد إنشاء Session String

### البوت يتوقف:
1. تحقق من "Deployments" في Railway
2. تأكد من أن النوع "Worker" وليس "Web"
3. تحقق من حدود الاستخدام (500 ساعة/شهر)

## 💡 نصائح مهمة

### للاستقرار:
- استخدم `requirements_cloud.txt` فقط
- تأكد من Start Command صحيح
- راقب السجلات أول يوم

### للأمان:
- لا تشارك Session String مع أحد
- استخدم Variables السرية في Railway
- احفظ نسخة احتياطية من المتغيرات

### للتوفير:
- راقب ساعات الاستخدام شهرياً
- استخدم كلمات مفتاحية محددة
- أوقف البوت إذا لم تعد تحتاجه

## 🎯 النتيجة النهائية

بعد اكتمال النشر:
- ✅ البوت يعمل 24/7 على السحابة
- ✅ يراقب جميع مجموعاتك تلقائياً
- ✅ يرسل تنبيهات فورية في Saved Messages
- ✅ لا أحد يعرف أنك تراقب
- ✅ مجاني تماماً (500 ساعة/شهر)

---

**🚀 ابدأ الآن: `python quick_deploy.py`**
