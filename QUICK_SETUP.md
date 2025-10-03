# ⚡ الإعداد السريع - 5 دقائق فقط!

## 🎯 **الخطوات الأساسية:**

### **1️⃣ احصل على API من تلجرام:**
- اذهب: https://my.telegram.org
- سجل دخول → API Development Tools
- احفظ: `API_ID` و `API_HASH`

### **2️⃣ أنشئ Session String:**
- شغل: `setup_userbot.py`
- أدخل API_ID, API_HASH, رقم الهاتف
- انسخ Session String الطويل

### **3️⃣ أنشئ مشروع Railway:**
- اذهب: https://railway.app
- New Project → Deploy from GitHub
- اختر: `saudi-userbot`

### **4️⃣ أضف المتغيرات:**
```
TELEGRAM_API_ID = 12345678
TELEGRAM_API_HASH = abc123def456
TELEGRAM_SESSION_STRING = 1BVtsOHwAA....
```

### **5️⃣ انتظر التشغيل:**
- Railway سيرفع البوت تلقائياً
- تحقق من Logs: "Cloud User bot is running"
- تحقق من Saved Messages للرسالة الترحيبية

---

## ✅ **تأكد من النجاح:**

### **في Saved Messages اكتب:**
```
#عرض
```
**يجب أن ترى:** قائمة الكلمات المفتاحية

### **في أي مجموعة اكتب:**
```
ابي حد يساعدني
```
**يجب أن تصلك:** إشعارات فورية

---

## 🎛️ **الأوامر الأساسية:**
- `+كلمة` - إضافة كلمة مفتاحية
- `-كلمة` - حذف كلمة مفتاحية  
- `#عرض` - عرض جميع الكلمات
- `!احصائيات` - عرض معلومات البوت

---

## 🚨 **إذا لم يعمل:**
1. تحقق من Railway Logs
2. تأكد من صحة Session String
3. تأكد أن الحساب في المجموعات المطلوبة

**🎉 مبروك! البوت جاهز للعمل!**
