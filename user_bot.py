#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Telegram User Bot for Monitoring Groups
Uses your personal account to monitor groups and send notifications
"""

import asyncio
import json
import logging
from datetime import datetime
from telethon import TelegramClient, events
from telethon.tl.types import PeerUser, PeerChat, PeerChannel
import os

# Configure logging
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)
logger = logging.getLogger(__name__)

class SaudiUserBot:
    def __init__(self, api_id: int, api_hash: str, phone: str):
        self.api_id = api_id
        self.api_hash = api_hash
        self.phone = phone
        self.client = TelegramClient('saudi_session', api_id, api_hash)
        
        # Default keywords
        self.keywords = [
            "يسوي", "يحل", "يساعدني", "ابي شخص", "تعرفون حد", 
            "ابي حد", "محتاج", "اريد", "اطلب", "ممكن حد",
            "ابغى", "ودي", "عايز", "بدي", "اريد واحد"
        ]
        
        self.monitored_groups = set()
        self.my_user_id = None
        self.load_config()
        
    def load_config(self):
        """Load configuration from file"""
        try:
            if os.path.exists('user_config.json'):
                with open('user_config.json', 'r', encoding='utf-8') as f:
                    config = json.load(f)
                    self.keywords = config.get('keywords', self.keywords)
                    self.monitored_groups = set(config.get('monitored_groups', []))
                    logger.info(f"Loaded {len(self.keywords)} keywords and {len(self.monitored_groups)} groups")
        except Exception as e:
            logger.error(f"Error loading config: {e}")
    
    def save_config(self):
        """Save configuration to file"""
        try:
            config = {
                'keywords': self.keywords,
                'monitored_groups': list(self.monitored_groups),
                'last_updated': datetime.now().isoformat()
            }
            with open('user_config.json', 'w', encoding='utf-8') as f:
                json.dump(config, f, ensure_ascii=False, indent=2)
            logger.info("Configuration saved")
        except Exception as e:
            logger.error(f"Error saving config: {e}")

    async def start(self):
        """Start the user bot"""
        await self.client.start(phone=self.phone)
        
        # Get my user ID
        me = await self.client.get_me()
        self.my_user_id = me.id
        logger.info(f"Started as {me.first_name} (ID: {me.id})")
        
        # Register event handlers
        self.client.add_event_handler(self.handle_new_message, events.NewMessage)
        
        # Send startup message to self
        await self.send_to_self("🤖 **بوت المراقبة بدأ العمل!**\n\n"
                               f"📊 **الإحصائيات:**\n"
                               f"🔑 الكلمات المفتاحية: {len(self.keywords)}\n"
                               f"👥 المجموعات المراقبة: {len(self.monitored_groups)}\n\n"
                               f"✅ البوت جاهز لمراقبة المجموعات!")
        
        logger.info("User bot is running...")

    async def handle_new_message(self, event):
        """Handle new messages in groups"""
        try:
            message = event.message
            
            # Skip if message is from me
            if message.sender_id == self.my_user_id:
                return
            
            # Only monitor group messages
            if not (hasattr(event.chat, 'title') and event.chat.title):
                return
                
            # Add group to monitored list
            group_id = event.chat_id
            if group_id not in self.monitored_groups:
                self.monitored_groups.add(group_id)
                self.save_config()
                logger.info(f"Added new group to monitoring: {event.chat.title}")
            
            # Check for keywords in message text
            if message.text:
                await self.check_keywords(message, event.chat)
                
        except Exception as e:
            logger.error(f"Error handling message: {e}")

    async def check_keywords(self, message, chat):
        """Check if message contains keywords"""
        text_lower = message.text.lower()
        found_keywords = []
        
        for keyword in self.keywords:
            if keyword.lower() in text_lower:
                found_keywords.append(keyword)
        
        if found_keywords:
            await self.send_notification(message, chat, found_keywords)

    async def send_notification(self, message, chat, keywords):
        """Send notification to self"""
        try:
            # Get sender info
            sender = await message.get_sender()
            sender_name = getattr(sender, 'first_name', 'غير معروف')
            sender_username = getattr(sender, 'username', None)
            
            # Create notification message
            notification = f"""
🚨 **رسالة جديدة تحتوي على كلمات مفتاحية!**

👥 **المجموعة:** {chat.title}
👤 **المرسل:** {sender_name}
🆔 **المعرف:** {'@' + sender_username if sender_username else 'لا يوجد'}
🔑 **الكلمات المفتاحية:** {', '.join(keywords)}
⏰ **الوقت:** {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}

📝 **الرسالة:**
{message.text}

---
💬 **للرد:** انقر على اسم المرسل أعلاه أو ابحث عن المعرف
🔗 **رابط المجموعة:** {f"https://t.me/c/{str(chat.id)[4:]}/{message.id}" if hasattr(chat, 'username') and chat.username else "رابط غير متاح"}
            """
            
            await self.send_to_self(notification)
            logger.info(f"Sent notification for message from {sender_name} in {chat.title}")
            
        except Exception as e:
            logger.error(f"Error sending notification: {e}")

    async def send_to_self(self, message):
        """Send message to self (Saved Messages)"""
        try:
            await self.client.send_message('me', message)
        except Exception as e:
            logger.error(f"Error sending to self: {e}")

    async def add_keyword(self, keyword):
        """Add new keyword"""
        if keyword not in self.keywords:
            self.keywords.append(keyword)
            self.save_config()
            await self.send_to_self(f"✅ تم إضافة الكلمة المفتاحية: **{keyword}**")
            return True
        else:
            await self.send_to_self(f"⚠️ الكلمة المفتاحية موجودة بالفعل: **{keyword}**")
            return False

    async def remove_keyword(self, keyword):
        """Remove keyword"""
        if keyword in self.keywords:
            self.keywords.remove(keyword)
            self.save_config()
            await self.send_to_self(f"✅ تم حذف الكلمة المفتاحية: **{keyword}**")
            return True
        else:
            await self.send_to_self(f"❌ الكلمة المفتاحية غير موجودة: **{keyword}**")
            return False

    async def show_stats(self):
        """Show statistics"""
        stats = f"""
📊 **إحصائيات بوت المراقبة:**

🔑 **الكلمات المفتاحية:** {len(self.keywords)}
👥 **المجموعات المراقبة:** {len(self.monitored_groups)}
⏰ **آخر تحديث:** {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}

📝 **الكلمات المفتاحية الحالية:**
{chr(10).join([f"• {keyword}" for keyword in self.keywords])}

💡 **نصيحة:** أرسل "إضافة: كلمة_جديدة" لإضافة كلمة مفتاحية
💡 **نصيحة:** أرسل "حذف: كلمة_موجودة" لحذف كلمة مفتاحية
        """
        await self.send_to_self(stats)

    async def handle_commands(self):
        """Handle commands sent to self"""
        @self.client.on(events.NewMessage(chats='me', from_users='me'))
        async def command_handler(event):
            text = event.message.text.strip()
            
            if text.startswith('إضافة:') or text.startswith('اضافة:'):
                keyword = text.split(':', 1)[1].strip()
                await self.add_keyword(keyword)
                
            elif text.startswith('حذف:'):
                keyword = text.split(':', 1)[1].strip()
                await self.remove_keyword(keyword)
                
            elif text == 'إحصائيات' or text == 'احصائيات':
                await self.show_stats()
                
            elif text == 'مساعدة' or text == 'help':
                help_text = """
🤖 **أوامر بوت المراقبة:**

📝 **إضافة كلمة مفتاحية:**
`إضافة: الكلمة_الجديدة`

🗑️ **حذف كلمة مفتاحية:**
`حذف: الكلمة_المراد_حذفها`

📊 **عرض الإحصائيات:**
`إحصائيات`

❓ **عرض المساعدة:**
`مساعدة`

💡 **ملاحظة:** أرسل هذه الأوامر في الرسائل المحفوظة (Saved Messages)
                """
                await self.send_to_self(help_text)

    async def run(self):
        """Run the user bot"""
        try:
            await self.start()
            await self.handle_commands()
            
            # Keep running
            await self.client.run_until_disconnected()
            
        except Exception as e:
            logger.error(f"Error running bot: {e}")
        finally:
            await self.client.disconnect()

def main():
    """Main function"""
    # Get credentials from environment or input
    API_ID = os.getenv('TELEGRAM_API_ID')
    API_HASH = os.getenv('TELEGRAM_API_HASH')
    PHONE = os.getenv('TELEGRAM_PHONE')
    
    if not API_ID:
        API_ID = input("أدخل API ID: ")
    if not API_HASH:
        API_HASH = input("أدخل API Hash: ")
    if not PHONE:
        PHONE = input("أدخل رقم الهاتف (مع رمز البلد): ")
    
    try:
        API_ID = int(API_ID)
    except ValueError:
        print("❌ API ID يجب أن يكون رقم")
        return
    
    # Create and run bot
    bot = SaudiUserBot(API_ID, API_HASH, PHONE)
    
    try:
        asyncio.run(bot.run())
    except KeyboardInterrupt:
        print("\n🛑 تم إيقاف البوت")
    except Exception as e:
        print(f"❌ خطأ: {e}")

if __name__ == '__main__':
    main()
