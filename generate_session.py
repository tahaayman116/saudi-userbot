#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Generate Telegram Session String for Cloud Deployment
Run this locally to get session string for cloud hosting
"""

import asyncio
import os
from telethon import TelegramClient
from telethon.sessions import StringSession

async def generate_session():
    """Generate session string for cloud deployment"""
    print("🔑 مولد Session String للاستضافة السحابية")
    print("=" * 50)
    
    # Get credentials
    api_id = input("أدخل API ID: ").strip()
    api_hash = input("أدخل API Hash: ").strip()
    
    try:
        api_id = int(api_id)
    except ValueError:
        print("❌ API ID يجب أن يكون رقم")
        return
    
    # Create client with string session
    client = TelegramClient(StringSession(), api_id, api_hash)
    
    try:
        print("\n📱 جاري تسجيل الدخول...")
        await client.start()
        
        # Get session string
        session_string = client.session.save()
        
        # Get user info
        me = await client.get_me()
        
        print(f"\n✅ تم تسجيل الدخول بنجاح!")
        print(f"👤 الاسم: {me.first_name}")
        print(f"📞 الهاتف: {me.phone}")
        
        print(f"\n🔐 Session String الخاص بك:")
        print("=" * 50)
        print(session_string)
        print("=" * 50)
        
        # Save to file
        with open('session_string.txt', 'w') as f:
            f.write(session_string)
        
        print(f"\n💾 تم حفظ Session String في ملف: session_string.txt")
        
        # Create environment variables template
        env_template = f"""# Environment Variables for Cloud Deployment
TELEGRAM_API_ID={api_id}
TELEGRAM_API_HASH={api_hash}
TELEGRAM_SESSION_STRING={session_string}
KEYWORDS=يسوي,يحل,يساعدني,ابي شخص,تعرفون حد,ابي حد,محتاج,اريد,اطلب,ممكن حد
"""
        
        with open('cloud_env.txt', 'w', encoding='utf-8') as f:
            f.write(env_template)
        
        print(f"📝 تم إنشاء ملف متغيرات البيئة: cloud_env.txt")
        
        print(f"\n📋 الخطوات التالية:")
        print("1. انسخ Session String أعلاه")
        print("2. أضفه كمتغير بيئة في الاستضافة السحابية")
        print("3. أضف باقي المتغيرات من ملف cloud_env.txt")
        print("4. ارفع cloud_userbot.py للاستضافة")
        
    except Exception as e:
        print(f"❌ خطأ: {e}")
    
    finally:
        await client.disconnect()

def main():
    """Main function"""
    print("⚠️  تحذير: شغل هذا البرنامج على جهازك الشخصي فقط!")
    print("⚠️  لا تشغله على الاستضافة السحابية!")
    print()
    
    confirm = input("هل تريد المتابعة؟ (y/n): ").lower()
    if confirm != 'y':
        print("تم الإلغاء")
        return
    
    try:
        asyncio.run(generate_session())
    except KeyboardInterrupt:
        print("\n🛑 تم الإلغاء")
    except Exception as e:
        print(f"❌ خطأ: {e}")

if __name__ == '__main__':
    main()
