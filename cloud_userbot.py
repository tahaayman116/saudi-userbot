#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Cloud-optimized Telegram User Bot for Free Hosting
Optimized for Railway, Render, and other cloud platforms
"""

import asyncio
import json
import logging
import os
import signal
import sys
from datetime import datetime
from telethon import TelegramClient, events
from telethon.sessions import StringSession
import base64

# Configure logging for cloud
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO,
    handlers=[
        logging.StreamHandler(sys.stdout)
    ]
)
logger = logging.getLogger(__name__)

class CloudUserBot:
    def __init__(self, api_id: int, api_hash: str, session_string: str = None):
        self.api_id = api_id
        self.api_hash = api_hash
        
        # Use string session for cloud deployment with optimized settings
        if session_string:
            self.client = TelegramClient(
                StringSession(session_string), 
                api_id, 
                api_hash,
                # Optimized for many groups
                flood_sleep_threshold=24,
                request_retries=5,
                connection_retries=5,
                retry_delay=1,
                auto_reconnect=True,
                sequential_updates=True
            )
        else:
            self.client = TelegramClient(StringSession(), api_id, api_hash)
        
        # Default keywords
        self.keywords = [
            "يسوي", "يحل", "يساعدني", "ابي شخص", "تعرفون حد", 
            "ابي حد", "محتاج", "اريد", "اطلب", "ممكن حد",
            "ابغى", "ودي", "عايز", "بدي", "اريد واحد", "محتاج واحد"
        ]
        
        # Try to create/find a private channel for notifications
        self.notification_channel = None
        
        self.monitored_groups = set()
        self.my_user_id = None
        self.running = True
        
        # Load config from environment or defaults
        self.load_cloud_config()
        
    def load_cloud_config(self):
        """Load configuration from environment variables"""
        try:
            # Load keywords from environment
            keywords_env = os.getenv('KEYWORDS')
            if keywords_env:
                self.keywords = [k.strip() for k in keywords_env.split(',')]
                
            logger.info(f"Loaded {len(self.keywords)} keywords from config")
        except Exception as e:
            logger.error(f"Error loading cloud config: {e}")

    async def start(self):
        """Start the user bot"""
        try:
            await self.client.start()
            
            # Get my user ID
            me = await self.client.get_me()
            self.my_user_id = me.id
            logger.info(f"Started as {me.first_name} (ID: {me.id})")
            
            # Enable catch up for missed messages (important for 900+ groups)
            await self.client.catch_up()
            
            # Try to create a private channel for better notifications
            await self.setup_notification_channel()
            
            # Register event handlers with filters for better performance
            self.client.add_event_handler(
                self.handle_new_message, 
                events.NewMessage(
                    incoming=True,  # Only incoming messages
                    from_users=None,  # From any user
                    chats=None,  # From any chat
                    blacklist_chats=False,  # Don't blacklist any chats
                    func=lambda e: e.is_group or e.is_channel  # Only groups and channels
                )
            )
            
            # Register handler for ALL messages in Saved Messages (including my own)
            self.client.add_event_handler(
                self.handle_command,
                events.NewMessage(
                    chats='me'  # Only from Saved Messages
                )
            )
            
            # Send startup message to self
            startup_msg = f"""🤖 **بوت المراقبة السحابي بدأ العمل!**

📊 **الإحصائيات:**
🔑 الكلمات المفتاحية: {len(self.keywords)}
☁️ يعمل على الخادم السحابي
🆔 معرف المستخدم: {me.id}

✅ البوت جاهز لمراقبة المجموعات!

🔍 **الكلمات المراقبة:**
{', '.join(self.keywords)}

💡 **للاختبار:** اكتب في أي مجموعة رسالة تحتوي على إحدى الكلمات أعلاه

🎛️ **أوامر التحكم (في Saved Messages):**
• `+كلمة` - إضافة كلمة واحدة
• `+كلمة1، كلمة2، كلمة3` - إضافة كلمات متعددة
• `-كلمة` - حذف كلمة واحدة
• `-كلمة1، كلمة2، كلمة3` - حذف كلمات متعددة
• `#عرض` - عرض جميع الكلمات
• `!احصائيات` - عرض إحصائيات البوت"""
            
            await self.send_to_self(startup_msg)
            logger.info("Startup message sent to Saved Messages")
            logger.info("Cloud User bot is running...")
            return True
            
        except Exception as e:
            logger.error(f"Error starting bot: {e}")
            return False

    async def setup_notification_channel(self):
        """Setup a private channel for better push notifications"""
        try:
            # Try to find existing notification channel
            async for dialog in self.client.iter_dialogs():
                if hasattr(dialog.entity, 'title') and dialog.entity.title == "🔔 إشعارات البوت":
                    self.notification_channel = dialog.entity
                    logger.info("Found existing notification channel")
                    return
            
            # Create new private channel if not found
            from telethon.tl.functions.channels import CreateChannelRequest
            result = await self.client(CreateChannelRequest(
                title="🔔 إشعارات البوت",
                about="قناة خاصة لإشعارات البوت - لا تحذفها",
                megagroup=False
            ))
            
            self.notification_channel = result.chats[0]
            logger.info("Created new notification channel")
            
        except Exception as e:
            logger.warning(f"Could not setup notification channel: {e}")
            self.notification_channel = None

    async def handle_command(self, event):
        """Handle commands in Saved Messages"""
        try:
            message = event.message
            
            # Skip if no text
            if not message.text:
                return
                
            text = message.text.strip()
            
            # Only process commands that start with +, -, #, !
            if not text.startswith(('+', '-', '#', '!')):
                return
            
            logger.info(f"Processing command: {text}")
            
            # Add keyword command: +كلمة
            if text.startswith('+'):
                keyword = text[1:].strip()
                
                # Check if multiple keywords (separated by comma, semicolon, or newline)
                if any(sep in keyword for sep in [',', '،', ';', '؛', '\n']):
                    # Multiple keywords
                    separators = [',', '،', ';', '؛', '\n']
                    keywords_to_add = [keyword]
                    
                    # Split by all possible separators
                    for sep in separators:
                        temp_list = []
                        for kw in keywords_to_add:
                            temp_list.extend([k.strip() for k in kw.split(sep) if k.strip()])
                        keywords_to_add = temp_list
                    
                    # Remove duplicates and empty strings
                    keywords_to_add = list(set([kw for kw in keywords_to_add if kw and kw not in self.keywords]))
                    
                    if keywords_to_add:
                        self.keywords.extend(keywords_to_add)
                        await self.save_keywords()
                        
                        keywords_list = '\n'.join([f"• `{kw}`" for kw in keywords_to_add])
                        response = f"""✅ **تم إضافة {len(keywords_to_add)} كلمة مفتاحية:**

{keywords_list}

📊 **العدد الإجمالي:** {len(self.keywords)} كلمة"""
                        await asyncio.sleep(0.5)
                        await self.client.send_message('me', response, parse_mode='markdown')
                        logger.info(f"Added {len(keywords_to_add)} keywords: {keywords_to_add}")
                    else:
                        response = "⚠️ **جميع الكلمات موجودة بالفعل أو فارغة**"
                        await asyncio.sleep(0.5)
                        await self.client.send_message('me', response, parse_mode='markdown')
                        
                else:
                    # Single keyword (original logic)
                    if keyword and keyword not in self.keywords:
                        self.keywords.append(keyword)
                        await self.save_keywords()
                        response = f"✅ **تم إضافة الكلمة المفتاحية:**\n`{keyword}`\n\n📊 **العدد الحالي:** {len(self.keywords)} كلمة"
                        await asyncio.sleep(0.5)
                        await self.client.send_message('me', response, parse_mode='markdown')
                        logger.info(f"Added keyword: {keyword}")
                    elif keyword in self.keywords:
                        response = f"⚠️ **الكلمة موجودة بالفعل:**\n`{keyword}`"
                        await asyncio.sleep(0.5)
                        await self.client.send_message('me', response, parse_mode='markdown')
                    else:
                        response = """❌ **خطأ:** يرجى كتابة كلمة صحيحة

**أمثلة:**
• `+يساعدني` - إضافة كلمة واحدة
• `+يساعدني، ابي حد، محتاج` - إضافة كلمات متعددة"""
                        await asyncio.sleep(0.5)
                        await self.client.send_message('me', response, parse_mode='markdown')
            
            # Remove keyword command: -كلمة
            elif text.startswith('-'):
                keyword = text[1:].strip()
                
                # Check if multiple keywords (separated by comma, semicolon, or newline)
                if any(sep in keyword for sep in [',', '،', ';', '؛', '\n']):
                    # Multiple keywords
                    separators = [',', '،', ';', '؛', '\n']
                    keywords_to_remove = [keyword]
                    
                    # Split by all possible separators
                    for sep in separators:
                        temp_list = []
                        for kw in keywords_to_remove:
                            temp_list.extend([k.strip() for k in kw.split(sep) if k.strip()])
                        keywords_to_remove = temp_list
                    
                    # Filter only existing keywords
                    existing_keywords = [kw for kw in keywords_to_remove if kw in self.keywords]
                    
                    if existing_keywords:
                        for kw in existing_keywords:
                            self.keywords.remove(kw)
                        await self.save_keywords()
                        
                        keywords_list = '\n'.join([f"• `{kw}`" for kw in existing_keywords])
                        response = f"""✅ **تم حذف {len(existing_keywords)} كلمة مفتاحية:**

{keywords_list}

📊 **العدد الإجمالي:** {len(self.keywords)} كلمة"""
                        await asyncio.sleep(0.5)
                        await self.client.send_message('me', response, parse_mode='markdown')
                        logger.info(f"Removed {len(existing_keywords)} keywords: {existing_keywords}")
                    else:
                        response = "⚠️ **لا توجد كلمات صحيحة للحذف**"
                        await asyncio.sleep(0.5)
                        await self.client.send_message('me', response, parse_mode='markdown')
                        
                else:
                    # Single keyword (original logic)
                    if keyword and keyword in self.keywords:
                        self.keywords.remove(keyword)
                        await self.save_keywords()
                        response = f"✅ **تم حذف الكلمة المفتاحية:**\n`{keyword}`\n\n📊 **العدد الحالي:** {len(self.keywords)} كلمة"
                        await asyncio.sleep(0.5)
                        await self.client.send_message('me', response, parse_mode='markdown')
                        logger.info(f"Removed keyword: {keyword}")
                    elif keyword not in self.keywords:
                        response = f"⚠️ **الكلمة غير موجودة:**\n`{keyword}`"
                        await asyncio.sleep(0.5)
                        await self.client.send_message('me', response, parse_mode='markdown')
                    else:
                        response = """❌ **خطأ:** يرجى كتابة كلمة صحيحة

**أمثلة:**
• `-يساعدني` - حذف كلمة واحدة
• `-يساعدني، ابي حد، محتاج` - حذف كلمات متعددة"""
                        await asyncio.sleep(0.5)
                        await self.client.send_message('me', response, parse_mode='markdown')
            
            # Show all keywords: #عرض
            elif text.startswith('#'):
                command = text[1:].strip().lower()
                if command in ['عرض', 'الكلمات', 'قائمة']:
                    if self.keywords:
                        keywords_list = '\n'.join([f"• `{kw}`" for kw in self.keywords])
                        response = f"""📋 **قائمة الكلمات المفتاحية:**

{keywords_list}

📊 **العدد الإجمالي:** {len(self.keywords)} كلمة

💡 **للإضافة:** `+كلمة_جديدة`
💡 **للحذف:** `-كلمة_موجودة`"""
                        await asyncio.sleep(0.5)
                        await self.client.send_message('me', response, parse_mode='markdown')
                    else:
                        response = "📋 **قائمة الكلمات المفتاحية فارغة**\n\n💡 **لإضافة كلمة:** `+كلمة_جديدة`"
                        await asyncio.sleep(0.5)
                        await self.client.send_message('me', response, parse_mode='markdown')
                else:
                    response = "❌ **أمر غير معروف**\n**الأوامر المتاحة:**\n• `#عرض` - عرض الكلمات"
                    await asyncio.sleep(0.5)
                    await self.client.send_message('me', response, parse_mode='markdown')
            
            # Statistics command: !احصائيات
            elif text.startswith('!'):
                command = text[1:].strip().lower()
                if command in ['احصائيات', 'معلومات', 'حالة']:
                    response = f"""📊 **إحصائيات البوت:**

🔑 **الكلمات المفتاحية:** {len(self.keywords)}
👥 **المجموعات المراقبة:** {len(self.monitored_groups)}
☁️ **الحالة:** يعمل على الخادم السحابي
🆔 **معرف المستخدم:** {self.my_user_id}

🎛️ **أوامر التحكم:**
• `+كلمة` - إضافة كلمة واحدة
• `+كلمة1، كلمة2، كلمة3` - إضافة كلمات متعددة
• `-كلمة` - حذف كلمة واحدة
• `-كلمة1، كلمة2، كلمة3` - حذف كلمات متعددة
• `#عرض` - عرض جميع الكلمات
• `!احصائيات` - عرض هذه المعلومات"""
                    await asyncio.sleep(0.5)
                    await self.client.send_message('me', response, parse_mode='markdown')
                else:
                    response = "❌ **أمر غير معروف**\n**الأوامر المتاحة:**\n• `!احصائيات` - عرض المعلومات"
                    await asyncio.sleep(0.5)
                    await self.client.send_message('me', response, parse_mode='markdown')
            
        except Exception as e:
            logger.error(f"Error handling command: {e}")
            await asyncio.sleep(0.5)
            await self.client.send_message('me', f"❌ **خطأ في تنفيذ الأمر:** {str(e)}")

    async def save_keywords(self):
        """Save keywords to environment or file"""
        try:
            # For now, just log the change
            logger.info(f"Keywords updated: {self.keywords}")
            # In a real deployment, you might want to save to a database or file
        except Exception as e:
            logger.error(f"Error saving keywords: {e}")

    async def handle_new_message(self, event):
        """Handle new messages in groups - optimized for 900+ groups"""
        try:
            message = event.message
            
            # Skip if message is from me
            if message.sender_id == self.my_user_id:
                return
            
            # Skip if no text
            if not message.text:
                return
                
            # Add group to monitored list (simplified)
            group_id = event.chat_id
            if group_id not in self.monitored_groups:
                self.monitored_groups.add(group_id)
                chat_name = getattr(event.chat, 'title', 'Unknown Group')
                logger.info(f"Monitoring new group: {chat_name} (Total: {len(self.monitored_groups)})")
            
            # Quick keyword check
            text_lower = message.text.lower()
            found_keywords = [kw for kw in self.keywords if kw.lower() in text_lower]
            
            if found_keywords:
                logger.info(f"🚨 MATCH! Keywords: {found_keywords} in group: {getattr(event.chat, 'title', 'Unknown')}")
                await self.send_notification(message, event.chat, found_keywords)
                
        except Exception as e:
            logger.error(f"Error handling message: {e}")


    async def send_notification(self, message, chat, keywords):
        """Send notification to self"""
        try:
            # Get sender info safely with better error handling
            sender = await message.get_sender()
            sender_name = getattr(sender, 'first_name', 'غير معروف')
            sender_username = getattr(sender, 'username', None)
            
            # Get sender ID with multiple fallbacks
            sender_id = None
            if hasattr(sender, 'id') and sender.id:
                sender_id = sender.id
            elif hasattr(message, 'sender_id') and message.sender_id:
                sender_id = message.sender_id
            elif hasattr(message, 'from_id') and message.from_id:
                if hasattr(message.from_id, 'user_id'):
                    sender_id = message.from_id.user_id
                else:
                    sender_id = message.from_id
            
            # If still no sender_id, skip this message
            if not sender_id:
                logger.warning(f"Could not get sender ID for message from {sender_name}")
                return
            
            # Get chat info safely
            chat_name = getattr(chat, 'title', getattr(chat, 'first_name', 'مجموعة غير معروفة'))
            
            # Try to get group link if available
            group_link = "غير متاح"
            if hasattr(chat, 'username') and chat.username:
                group_link = f"https://t.me/{chat.username}"
            elif hasattr(chat, 'id'):
                # Create internal link for private groups
                group_link = f"tg://openmessage?chat_id={chat.id}&message_id={message.id}"
            
            # Create clickable notification with verified sender_id
            clickable_notification = f"""🚨 **رسالة جديدة تحتوي على كلمات مفتاحية!**

👥 **المجموعة:** {chat_name}
👤 **المرسل:** {sender_name}
🆔 **المعرف:** {'@' + sender_username if sender_username else f'ID: {sender_id}'}
🔑 **الكلمات المفتاحية:** {', '.join(keywords)}
⏰ **الوقت:** {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
☁️ **المصدر:** خادم سحابي

📝 **الرسالة الكاملة:**
{message.text}

---
💬 **[اضغط هنا للذهاب للشخص](tg://user?id={sender_id})**

🔗 **أو ابحث عن المعرف:** {'@' + sender_username if sender_username else f'ID: {sender_id}'}
📱 **رابط الرسالة:** {group_link}

🔥 **للتواصل السريع انسخ هذا الرابط:**
`tg://user?id={sender_id}`"""
            
            await self.client.send_message('me', clickable_notification, parse_mode='markdown')
            logger.info(f"✅ Sent clickable notification for message from {sender_name} (ID: {sender_id}) in {chat_name}")
            
            # Create push notification with better contact method
            push_notification = f"""🔔 **إشعار كلمة مفتاحية!**

🚨 **{', '.join(keywords)}**
👤 **{sender_name}**
👥 **{chat_name}**

📝 **الرسالة الكاملة:**
{message.text}

💬 **للتواصل:**
{'@' + sender_username if sender_username else f'انسخ: tg://user?id={sender.id}'}"""
            
            # Create push notification with clickable link
            push_with_link = f"""🔔 **إشعار كلمة مفتاحية!**

🚨 **{', '.join(keywords)}**
👤 **{sender_name}**
👥 **{chat_name}**

📝 **الرسالة الكاملة:**
{message.text}

💬 **[اضغط للتواصل مع الشخص](tg://user?id={sender_id})**

🔥 **أو انسخ الرابط:**
`tg://user?id={sender_id}`"""
            
            # Send to self using user ID (this triggers notifications better than 'me')
            await self.client.send_message(self.my_user_id, push_with_link, parse_mode='markdown')
            logger.info("✅ Sent push notification with clickable link")
            
            # Also try sending a simple text message for maximum notification visibility
            simple_alert = f"🚨 {', '.join(keywords)} من {sender_name} في {chat_name}"
            await self.client.send_message(self.my_user_id, simple_alert)
            logger.info("✅ Sent simple alert notification")
            
            # If notification channel exists, send there too (channels give better notifications)
            if self.notification_channel:
                channel_with_link = f"""🔔 **إشعار جديد!**

🚨 **{', '.join(keywords)}**
👤 من: **{sender_name}**
👥 في: **{chat_name}**

📝 **الرسالة الكاملة:**
{message.text}

💬 **[اضغط للذهاب للشخص](tg://user?id={sender_id})**

🔗 **أو انسخ الرابط:**
`tg://user?id={sender_id}`"""
                
                await self.client.send_message(self.notification_channel, channel_with_link, parse_mode='markdown')
                logger.info("✅ Sent notification to private channel with clickable link")
            
        except Exception as e:
            logger.error(f"❌ Error sending notification: {e}")
            # Try simple notification as backup
            try:
                simple_msg = f"""🚨 كلمة مفتاحية: {', '.join(keywords)}

👤 من: {sender_name}
👥 في: {chat_name}

📝 الرسالة الكاملة:
{message.text}

💬 للتواصل: {'@' + sender_username if sender_username else f'tg://user?id={sender.id}'}"""
                await self.send_to_self(simple_msg)
                logger.info("✅ Sent simple notification as backup")
            except Exception as e2:
                logger.error(f"❌ Backup notification also failed: {e2}")

    async def send_to_self(self, message):
        """Send message to self (Saved Messages)"""
        try:
            await self.client.send_message('me', message)
            logger.info("Message sent to Saved Messages successfully")
        except Exception as e:
            logger.error(f"Error sending to self: {e}")
            # Try alternative method
            try:
                await self.client.send_message(self.my_user_id, message)
                logger.info("Message sent using user ID successfully")
            except Exception as e2:
                logger.error(f"Alternative send method also failed: {e2}")

    async def handle_shutdown(self):
        """Handle graceful shutdown"""
        logger.info("Shutting down bot...")
        self.running = False
        if self.client.is_connected():
            await self.client.disconnect()

    async def run(self):
        """Run the user bot with proper error handling"""
        try:
            # Start the bot
            if not await self.start():
                logger.error("Failed to start bot")
                return
            
            # Keep running until shutdown
            while self.running:
                await asyncio.sleep(1)
                
        except Exception as e:
            logger.error(f"Error in main loop: {e}")
        finally:
            await self.handle_shutdown()

def signal_handler(signum, frame):
    """Handle shutdown signals"""
    logger.info(f"Received signal {signum}")
    sys.exit(0)

async def main():
    """Main function for cloud deployment"""
    # Set up signal handlers
    signal.signal(signal.SIGTERM, signal_handler)
    signal.signal(signal.SIGINT, signal_handler)
    
    # Get credentials from environment
    API_ID = os.getenv('TELEGRAM_API_ID')
    API_HASH = os.getenv('TELEGRAM_API_HASH')
    SESSION_STRING = os.getenv('TELEGRAM_SESSION_STRING')
    
    if not API_ID or not API_HASH:
        logger.error("Missing TELEGRAM_API_ID or TELEGRAM_API_HASH environment variables")
        return
    
    if not SESSION_STRING:
        logger.error("Missing TELEGRAM_SESSION_STRING environment variable")
        logger.info("Run generate_session.py locally to get session string")
        return
    
    try:
        API_ID = int(API_ID)
    except ValueError:
        logger.error("TELEGRAM_API_ID must be a number")
        return
    
    # Create and run bot
    bot = CloudUserBot(API_ID, API_HASH, SESSION_STRING)
    
    try:
        await bot.run()
    except KeyboardInterrupt:
        logger.info("Bot stopped by user")
    except Exception as e:
        logger.error(f"Bot crashed: {e}")
        # Auto-restart in cloud environment
        await asyncio.sleep(5)
        await main()

if __name__ == '__main__':
    # Run the bot
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        logger.info("Bot stopped")
    except Exception as e:
        logger.error(f"Fatal error: {e}")
        sys.exit(1)
