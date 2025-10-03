#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Debug Version - Telegram User Bot with Enhanced Debugging
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

# Enhanced logging
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.DEBUG,  # More detailed logging
    handlers=[
        logging.StreamHandler(sys.stdout)
    ]
)
logger = logging.getLogger(__name__)

class DebugUserBot:
    def __init__(self, api_id: int, api_hash: str, session_string: str = None):
        self.api_id = api_id
        self.api_hash = api_hash
        
        # Simple client setup
        if session_string:
            self.client = TelegramClient(StringSession(session_string), api_id, api_hash)
        else:
            self.client = TelegramClient(StringSession(), api_id, api_hash)
        
        # Simple keywords for testing
        self.keywords = ["يسوي", "يحل", "يساعدني", "ابي", "محتاج", "اريد", "test", "تست"]
        self.my_user_id = None
        self.running = True
        self.message_count = 0
        self.match_count = 0
        
    async def start(self):
        """Start the debug bot"""
        try:
            logger.info("🚀 Starting debug bot...")
            await self.client.start()
            
            # Get my info
            me = await self.client.get_me()
            self.my_user_id = me.id
            logger.info(f"✅ Logged in as: {me.first_name} (ID: {me.id})")
            
            # Test sending to self immediately
            test_msg = f"""🧪 **DEBUG BOT TEST MESSAGE**

⏰ Time: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
🆔 User ID: {me.id}
📱 Phone: {me.phone}

🔍 Keywords: {', '.join(self.keywords)}

✅ If you see this message, sending to Saved Messages works!
🧪 Now testing group monitoring..."""

            logger.info("📤 Sending test message to Saved Messages...")
            await self.client.send_message('me', test_msg)
            logger.info("✅ Test message sent successfully!")
            
            # Register simple event handler
            @self.client.on(events.NewMessage)
            async def handle_message(event):
                await self.debug_message_handler(event)
            
            logger.info("🎯 Event handler registered")
            logger.info("🔍 Bot is now monitoring all messages...")
            
            return True
            
        except Exception as e:
            logger.error(f"❌ Error starting bot: {e}")
            import traceback
            logger.error(traceback.format_exc())
            return False

    async def debug_message_handler(self, event):
        """Debug message handler with detailed logging"""
        try:
            self.message_count += 1
            message = event.message
            
            # Skip my own messages
            if message.sender_id == self.my_user_id:
                return
            
            # Log every message for debugging
            chat_info = "Unknown"
            if hasattr(event.chat, 'title'):
                chat_info = f"Group: {event.chat.title}"
            elif hasattr(event.chat, 'first_name'):
                chat_info = f"Private: {event.chat.first_name}"
            
            logger.info(f"📨 Message #{self.message_count} from {chat_info}")
            
            # Only process text messages
            if not message.text:
                logger.debug("⏭️ Skipping non-text message")
                return
            
            # Log message content (first 100 chars)
            logger.info(f"📝 Content: {message.text[:100]}...")
            
            # Check for keywords
            text_lower = message.text.lower()
            found_keywords = []
            
            for keyword in self.keywords:
                if keyword.lower() in text_lower:
                    found_keywords.append(keyword)
            
            if found_keywords:
                self.match_count += 1
                logger.info(f"🎯 KEYWORD MATCH #{self.match_count}!")
                logger.info(f"🔑 Found keywords: {found_keywords}")
                logger.info(f"📍 In chat: {chat_info}")
                
                # Send notification
                await self.send_debug_notification(message, event.chat, found_keywords)
            else:
                logger.debug(f"❌ No keywords found in: {text_lower[:50]}...")
                
        except Exception as e:
            logger.error(f"💥 Error in message handler: {e}")
            import traceback
            logger.error(traceback.format_exc())

    async def send_debug_notification(self, message, chat, keywords):
        """Send debug notification"""
        try:
            logger.info("📤 Preparing notification...")
            
            # Get sender info
            sender = await message.get_sender()
            sender_name = getattr(sender, 'first_name', 'Unknown')
            sender_username = getattr(sender, 'username', None)
            
            # Get chat info
            chat_name = getattr(chat, 'title', getattr(chat, 'first_name', 'Unknown'))
            
            # Create notification
            notification = f"""🚨 **KEYWORD MATCH DETECTED!**

👥 **Chat:** {chat_name}
👤 **Sender:** {sender_name}
🆔 **Username:** {'@' + sender_username if sender_username else 'None'}
🔑 **Keywords:** {', '.join(keywords)}
⏰ **Time:** {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
📊 **Match #:** {self.match_count}

📝 **Message:**
{message.text}

---
🧪 **DEBUG INFO:**
- Message ID: {message.id}
- Chat ID: {chat.id}
- Sender ID: {sender.id}
"""
            
            logger.info("📤 Sending notification to Saved Messages...")
            await self.client.send_message('me', notification)
            logger.info("✅ Notification sent successfully!")
            
            # Also log to console
            logger.info(f"🎉 SUCCESS! Sent notification for match #{self.match_count}")
            
        except Exception as e:
            logger.error(f"💥 Error sending notification: {e}")
            import traceback
            logger.error(traceback.format_exc())
            
            # Try alternative method
            try:
                logger.info("🔄 Trying alternative send method...")
                simple_msg = f"🚨 MATCH: {', '.join(keywords)} in {getattr(chat, 'title', 'Unknown')}"
                await self.client.send_message(self.my_user_id, simple_msg)
                logger.info("✅ Alternative method worked!")
            except Exception as e2:
                logger.error(f"💥 Alternative method also failed: {e2}")

    async def run(self):
        """Run the debug bot"""
        try:
            if not await self.start():
                logger.error("❌ Failed to start bot")
                return
            
            logger.info("🔄 Bot running... Press Ctrl+C to stop")
            
            # Keep running
            while self.running:
                await asyncio.sleep(1)
                
                # Log stats every 60 seconds
                if self.message_count > 0 and self.message_count % 100 == 0:
                    logger.info(f"📊 Stats: {self.message_count} messages processed, {self.match_count} matches found")
                
        except Exception as e:
            logger.error(f"💥 Error in main loop: {e}")
        finally:
            logger.info("🛑 Shutting down...")
            if self.client.is_connected():
                await self.client.disconnect()

async def main():
    """Main function"""
    # Get credentials
    API_ID = os.getenv('TELEGRAM_API_ID')
    API_HASH = os.getenv('TELEGRAM_API_HASH')
    SESSION_STRING = os.getenv('TELEGRAM_SESSION_STRING')
    
    if not all([API_ID, API_HASH, SESSION_STRING]):
        logger.error("❌ Missing environment variables!")
        return
    
    try:
        API_ID = int(API_ID)
    except ValueError:
        logger.error("❌ API_ID must be a number")
        return
    
    # Create and run debug bot
    bot = DebugUserBot(API_ID, API_HASH, SESSION_STRING)
    
    try:
        await bot.run()
    except KeyboardInterrupt:
        logger.info("🛑 Bot stopped by user")
    except Exception as e:
        logger.error(f"💥 Fatal error: {e}")

if __name__ == '__main__':
    asyncio.run(main())
