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
            
            # Send startup message to self
            startup_msg = f"""🤖 **بوت المراقبة السحابي بدأ العمل!**

📊 **الإحصائيات:**
🔑 الكلمات المفتاحية: {len(self.keywords)}
☁️ يعمل على الخادم السحابي
🆔 معرف المستخدم: {me.id}

✅ البوت جاهز لمراقبة المجموعات!

🔍 **الكلمات المراقبة:**
{', '.join(self.keywords)}

💡 **للاختبار:** اكتب في أي مجموعة رسالة تحتوي على إحدى الكلمات أعلاه"""
            
            await self.send_to_self(startup_msg)
            logger.info("Startup message sent to Saved Messages")
            logger.info("Cloud User bot is running...")
            return True
            
        except Exception as e:
            logger.error(f"Error starting bot: {e}")
            return False

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
☁️ **المصدر:** خادم سحابي

📝 **الرسالة:**
{message.text}

---
💬 **للرد:** {'@' + sender_username if sender_username else f"tg://user?id={sender.id}"}
            """
            
            await self.send_to_self(notification)
            logger.info(f"Sent cloud notification for message from {sender_name} in {chat.title}")
            
        except Exception as e:
            logger.error(f"Error sending notification: {e}")

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
