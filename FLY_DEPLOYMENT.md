# 🚀 دليل النشر على Fly.io

## خطوات النشر السريع

### 1. تسجيل الدخول إلى Fly.io
```bash
flyctl auth signup
# أو إذا كان لديك حساب:
flyctl auth login
```

### 2. إضافة المتغيرات السرية (Secrets)
```bash
flyctl secrets set TELEGRAM_API_ID=your_api_id
flyctl secrets set TELEGRAM_API_HASH=your_api_hash
flyctl secrets set TELEGRAM_SESSION_STRING=your_session_string
```

### 3. نشر البوت
```bash
flyctl launch
flyctl deploy
```

### 4. التحقق من عمل البوت
```bash
flyctl logs
flyctl status
```

## المتغيرات المطلوبة

احصل على هذه القيم قبل النشر:

- **TELEGRAM_API_ID**: من https://my.telegram.org
- **TELEGRAM_API_HASH**: من https://my.telegram.org
- **TELEGRAM_SESSION_STRING**: من ملف `session_string.txt`

## الملفات المضافة

- ✅ `fly.toml` - ملف التكوين الرئيسي
- ✅ `Dockerfile` - لبناء صورة Docker
- ✅ `.dockerignore` - لاستبعاد الملفات غير الضرورية

## الأوامر المفيدة

```bash
# عرض السجلات المباشرة
flyctl logs

# عرض حالة التطبيق
flyctl status

# إعادة نشر بعد التعديلات
flyctl deploy

# إيقاف التطبيق
flyctl apps destroy saudi-userbot
```

## استكشاف الأخطاء

### خطأ في البناء
```bash
flyctl logs
```

### تحديث المتغيرات
```bash
flyctl secrets set VARIABLE_NAME=new_value
```

### إعادة النشر
```bash
flyctl deploy --force
```

## المميزات المجانية

- ✅ 3 GB RAM
- ✅ 160 GB نقل بيانات شهرياً
- ✅ عمل مستمر 24/7
- ✅ بدون بطاقة دفع
