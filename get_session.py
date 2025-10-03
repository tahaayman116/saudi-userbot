#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Session String Generator - مولد Session String
"""

from telethon import TelegramClient
from telethon.sessions import StringSession

def get_session_string():
    """Generate Telegram Session String"""
    
    print("🔑 مولد Session String لتلجرام")
    print("=" * 40)
    
    # Get API credentials
    try:
        api_id = int(input("📝 أدخل API_ID: "))
        api_hash = input("📝 أدخل API_HASH: ")
        
        if not api_id or not api_hash:
            print("❌ يجب إدخال API_ID و API_HASH")
            return
            
    except ValueError:
        print("❌ API_ID يجب أن يكون رقم")
        return
    
    # Create client with empty session
    client = TelegramClient(StringSession(), api_id, api_hash)
    
    async def main():
        try:
            # Start client
            await client.start()
            
            # Get user info
            me = await client.get_me()
            print(f"\n✅ تم تسجيل الدخول بنجاح!")
            print(f"👤 الاسم: {me.first_name}")
            print(f"🆔 المعرف: {me.id}")
            
            # Get session string
            session_string = client.session.save()
            
            print(f"\n🎉 Session String الخاص بك:")
            print("=" * 50)
            print(session_string)
            print("=" * 50)
            
            print(f"\n⚠️ تحذيرات مهمة:")
            print("• احفظ هذا النص في مكان آمن")
            print("• لا تشاركه مع أحد أبداً")
            print("• استخدمه في متغيرات البيئة فقط")
            
            # Save to file
            with open('session_string.txt', 'w', encoding='utf-8') as f:
                f.write(session_string)
            print(f"\n💾 تم حفظ Session String في ملف: session_string.txt")
            
        except Exception as e:
            print(f"❌ خطأ: {e}")
        finally:
            await client.disconnect()
    
    # Run the client
    import asyncio
    asyncio.run(main())

if __name__ == "__main__":
    get_session_string()
