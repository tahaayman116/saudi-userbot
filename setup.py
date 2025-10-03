#!/usr/bin/env python3
"""
Setup script for Saudi Telegram Bot
"""

import os
import sys

def create_env_file():
    """Create .env file from template"""
    if os.path.exists('.env'):
        print("✅ ملف .env موجود بالفعل")
        return
    
    if os.path.exists('.env.example'):
        # Copy example to .env
        with open('.env.example', 'r') as f:
            content = f.read()
        
        with open('.env', 'w') as f:
            f.write(content)
        
        print("✅ تم إنشاء ملف .env")
        print("⚠️  يرجى تعديل ملف .env وإضافة التوكن ومعرف المستخدم")
    else:
        print("❌ ملف .env.example غير موجود")

def check_requirements():
    """Check if requirements are installed"""
    try:
        import telegram
        print("✅ مكتبة python-telegram-bot مثبتة")
    except ImportError:
        print("❌ مكتبة python-telegram-bot غير مثبتة")
        print("تشغيل: pip install -r requirements.txt")
        return False
    
    return True

def main():
    """Main setup function"""
    print("🚀 إعداد بوت تلجرام السعودي")
    print("=" * 40)
    
    # Check Python version
    if sys.version_info < (3, 8):
        print("❌ يتطلب Python 3.8 أو أحدث")
        return
    
    print(f"✅ Python {sys.version_info.major}.{sys.version_info.minor}")
    
    # Create .env file
    create_env_file()
    
    # Check requirements
    if not check_requirements():
        print("\n📦 لتثبيت المتطلبات:")
        print("pip install -r requirements.txt")
        return
    
    print("\n🎉 الإعداد مكتمل!")
    print("\n📋 الخطوات التالية:")
    print("1. عدل ملف .env وأضف التوكن ومعرف المستخدم")
    print("2. شغل البوت: python bot.py")
    print("3. أو انشر على Railway باستخدام railway_bot.py")

if __name__ == '__main__':
    main()
