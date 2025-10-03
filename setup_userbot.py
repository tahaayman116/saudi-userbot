#!/usr/bin/env python3
"""
Setup script for Telegram User Bot
"""

import os
import sys

def get_api_credentials():
    """Guide user to get API credentials"""
    print("🔑 للحصول على API ID و API Hash:")
    print("1. اذهب إلى https://my.telegram.org")
    print("2. سجل دخول برقم هاتفك")
    print("3. اذهب إلى 'API Development tools'")
    print("4. أنشئ تطبيق جديد")
    print("5. احفظ API ID و API Hash")
    print()

def create_env_file():
    """Create .env file for user bot"""
    if os.path.exists('.env'):
        print("✅ ملف .env موجود بالفعل")
        return
    
    get_api_credentials()
    
    api_id = input("أدخل API ID: ").strip()
    api_hash = input("أدخل API Hash: ").strip()
    phone = input("أدخل رقم الهاتف (مع رمز البلد، مثل: +966501234567): ").strip()
    
    env_content = f"""# Telegram User Bot Configuration
TELEGRAM_API_ID={api_id}
TELEGRAM_API_HASH={api_hash}
TELEGRAM_PHONE={phone}
"""
    
    with open('.env', 'w', encoding='utf-8') as f:
        f.write(env_content)
    
    print("✅ تم إنشاء ملف .env")

def check_requirements():
    """Check if requirements are installed"""
    try:
        import telethon
        print("✅ مكتبة Telethon مثبتة")
        return True
    except ImportError:
        print("❌ مكتبة Telethon غير مثبتة")
        print("تشغيل: pip install -r requirements_userbot.txt")
        return False

def main():
    """Main setup function"""
    print("🤖 إعداد User Bot للمراقبة")
    print("=" * 40)
    
    # Check Python version
    if sys.version_info < (3.8):
        print("❌ يتطلب Python 3.8 أو أحدث")
        return
    
    print(f"✅ Python {sys.version_info.major}.{sys.version_info.minor}")
    
    # Check requirements
    if not check_requirements():
        print("\n📦 لتثبيت المتطلبات:")
        print("pip install -r requirements_userbot.txt")
        return
    
    # Create .env file
    create_env_file()
    
    print("\n🎉 الإعداد مكتمل!")
    print("\n📋 الخطوات التالية:")
    print("1. شغل البوت: python user_bot.py")
    print("2. سيطلب منك رمز التحقق من تلجرام")
    print("3. بعد تسجيل الدخول، البوت سيبدأ المراقبة")
    print("4. ستصلك التنبيهات في الرسائل المحفوظة (Saved Messages)")
    
    print("\n💡 أوامر مفيدة في الرسائل المحفوظة:")
    print("• إضافة: كلمة_جديدة")
    print("• حذف: كلمة_موجودة") 
    print("• إحصائيات")
    print("• مساعدة")

if __name__ == '__main__':
    main()
