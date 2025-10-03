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
        
        # Use string session for cloud deployment
        if session_string:
            self.client = TelegramClient(StringSession(session_string), api_id, api_hash)
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
            
            # Register event handlers
            self.client.add_event_handler(self.handle_new_message, events.NewMessage)
            
            # Send startup message to self
            await self.send_to_self("🤖 **بوت المراقبة السحابي بدأ العمل!**\n\n"
                                   f"📊 **الإحصائيات:**\n"
                                   f"🔑 الكلمات المفتاحية: {len(self.keywords)}\n"
                                   f"☁️ يعمل على الخادم السحابي\n\n"
                                   f"✅ البوت جاهز لمراقبة المجموعات!")
            
            logger.info("Cloud User bot is running...")
            return True
            
        except Exception as e:
            logger.error(f"Error starting bot: {e}")
            return False

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
        except Exception as e:
            logger.error(f"Error sending to self: {e}")

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
