#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Quick Cloud Deployment Setup
إعداد سريع للنشر السحابي
"""

import os
import asyncio
from telethon import TelegramClient
from telethon.sessions import StringSession

async def quick_setup():
    """إعداد سريع للنشر السحابي"""
    print("🚀 إعداد سريع للنشر السحابي")
    print("=" * 40)
    
    # الحصول على البيانات
    print("📋 احتاج البيانات التالية:")
    api_id = input("API ID: ").strip()
    api_hash = input("API Hash: ").strip()
    
    try:
        api_id = int(api_id)
    except ValueError:
        print("❌ API ID يجب أن يكون رقم")
        return
    
    print("\n📱 جاري تسجيل الدخول...")
    
    # إنشاء session string
    client = TelegramClient(StringSession(), api_id, api_hash)
    
    try:
        await client.start()
        session_string = client.session.save()
        me = await client.get_me()
        
        print(f"✅ تم تسجيل الدخول: {me.first_name}")
        
        # إنشاء ملف متغيرات البيئة للنشر
        env_vars = f"""# متغيرات البيئة للنشر السحابي
# انسخ هذه القيم وأضفها في لوحة تحكم الاستضافة

TELEGRAM_API_ID={api_id}
TELEGRAM_API_HASH={api_hash}
TELEGRAM_SESSION_STRING={session_string}
KEYWORDS=يسوي,يحل,يساعدني,ابي شخص,تعرفون حد,ابي حد,محتاج,اريد,اطلب,ممكن حد,ابغى,ودي,عايز,بدي
"""
        
        # حفظ في ملف
        with open('DEPLOY_VARS.txt', 'w', encoding='utf-8') as f:
            f.write(env_vars)
        
        print("\n📝 تم إنشاء ملف DEPLOY_VARS.txt")
        print("📋 انسخ محتويات الملف وأضفها في لوحة تحكم الاستضافة")
        
        # عرض الخطوات التالية
        print("\n🎯 الخطوات التالية:")
        print("1. ارفع الكود على GitHub")
        print("2. اذهب إلى railway.app أو render.com")
        print("3. أنشئ مشروع جديد من GitHub")
        print("4. أضف متغيرات البيئة من ملف DEPLOY_VARS.txt")
        print("5. تأكد من أن النوع 'Worker' وليس 'Web'")
        print("6. Start Command: python cloud_userbot.py")
        
        # إنشاء ملف git commands
        git_commands = """# أوامر Git للرفع
git init
git add .
git commit -m "Saudi User Bot - Cloud Ready"
git branch -M main
git remote add origin https://github.com/USERNAME/REPO_NAME.git
git push -u origin main

# استبدل USERNAME و REPO_NAME بالقيم الصحيحة
"""
        
        with open('GIT_COMMANDS.txt', 'w', encoding='utf-8') as f:
            f.write(git_commands)
        
        print("\n📂 تم إنشاء ملف GIT_COMMANDS.txt مع أوامر Git")
        
        # إرسال رسالة تأكيد للنفس
        await client.send_message('me', 
            "🤖 **إعداد النشر السحابي مكتمل!**\n\n"
            "✅ تم إنشاء Session String بنجاح\n"
            "📝 تم حفظ متغيرات البيئة في DEPLOY_VARS.txt\n"
            "🚀 جاهز للنشر على السحابة!\n\n"
            "**الخطوة التالية:** ارفع الكود ونشر على Railway أو Render"
        )
        
        print("✅ تم إرسال تأكيد في الرسائل المحفوظة")
        
    except Exception as e:
        print(f"❌ خطأ: {e}")
    finally:
        await client.disconnect()

def main():
    """الدالة الرئيسية"""
    print("⚠️  تأكد من حصولك على API ID و API Hash من my.telegram.org")
    print("⚠️  ستحتاج رمز التحقق من تلجرام")
    print()
    
    confirm = input("جاهز للبدء؟ (y/n): ").lower()
    if confirm != 'y':
        print("تم الإلغاء")
        return
    
    try:
        asyncio.run(quick_setup())
        
        print("\n🎉 الإعداد مكتمل!")
        print("📁 تحقق من الملفات:")
        print("  • DEPLOY_VARS.txt - متغيرات البيئة")
        print("  • GIT_COMMANDS.txt - أوامر Git")
        
    except KeyboardInterrupt:
        print("\n🛑 تم الإلغاء")
    except Exception as e:
        print(f"❌ خطأ: {e}")

if __name__ == '__main__':
    main()
