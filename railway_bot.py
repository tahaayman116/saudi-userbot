#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Railway Deployment Version - Telegram Bot for Monitoring Group Messages
"""

import os
import logging
import json
from datetime import datetime
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes, CallbackQueryHandler
import asyncio

# Configure logging
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)
logger = logging.getLogger(__name__)

class SaudiBot:
    def __init__(self, token: str, owner_id: int):
        self.token = token
        self.owner_id = owner_id
        self.keywords = [
            "يسوي", "يحل", "يساعدني", "ابي شخص", "تعرفون حد", 
            "ابي حد", "محتاج", "اريد", "اطلب", "ممكن حد"
        ]
        self.monitored_groups = set()
        
    async def start(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Handle /start command"""
        user_id = update.effective_user.id
        
        if user_id == self.owner_id:
            welcome_text = """
🤖 مرحباً بك في بوت مراقبة المجموعات!

الأوامر المتاحة:
/keywords - عرض الكلمات المفتاحية
/groups - عرض المجموعات المراقبة
/stats - إحصائيات البوت
/help - المساعدة

البوت جاهز لمراقبة المجموعات! 🚀
            """
        else:
            welcome_text = "مرحباً! هذا بوت خاص للمراقبة."
            
        await update.message.reply_text(welcome_text)

    async def help_command(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Handle /help command"""
        if update.effective_user.id != self.owner_id:
            return
            
        help_text = """
📋 دليل استخدام البوت:

🔍 **المراقبة:**
- أضف البوت للمجموعات التي تريد مراقبتها
- البوت سيراقب الرسائل تلقائياً
- عند العثور على كلمة مفتاحية، سيرسل لك الرسالة

⚙️ **الإعدادات:**
/keywords - عرض الكلمات المفتاحية
/groups - عرض المجموعات المراقبة
/stats - عرض الإحصائيات

💡 **نصائح:**
- تأكد من إعطاء البوت صلاحية قراءة الرسائل
- البوت يعمل مع النصوص العربية والإنجليزية
        """
        await update.message.reply_text(help_text)

    async def keywords_command(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Handle /keywords command"""
        if update.effective_user.id != self.owner_id:
            return
            
        keywords_text = "🔑 الكلمات المفتاحية الحالية:\n\n"
        for i, keyword in enumerate(self.keywords, 1):
            keywords_text += f"{i}. {keyword}\n"
        await update.message.reply_text(keywords_text)

    async def groups_command(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Handle /groups command"""
        if update.effective_user.id != self.owner_id:
            return
            
        if not self.monitored_groups:
            await update.message.reply_text("📭 لا توجد مجموعات مراقبة حالياً")
            return
            
        groups_text = "📊 المجموعات المراقبة:\n\n"
        for i, group_id in enumerate(self.monitored_groups, 1):
            groups_text += f"{i}. Group ID: {group_id}\n"
            
        await update.message.reply_text(groups_text)

    async def stats_command(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Handle /stats command"""
        if update.effective_user.id != self.owner_id:
            return
            
        stats_text = f"""
📊 إحصائيات البوت:

🔑 عدد الكلمات المفتاحية: {len(self.keywords)}
👥 عدد المجموعات المراقبة: {len(self.monitored_groups)}
⏰ آخر تحديث: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}

الكلمات المفتاحية الحالية:
{', '.join(self.keywords)}
        """
        await update.message.reply_text(stats_text)

    async def monitor_messages(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Monitor group messages for keywords"""
        message = update.message
        
        # Skip if message is from owner or bot
        if message.from_user.id == self.owner_id or message.from_user.is_bot:
            return
            
        # Only monitor group messages
        if message.chat.type not in ['group', 'supergroup']:
            return
            
        # Add group to monitored groups
        group_id = message.chat.id
        self.monitored_groups.add(group_id)
            
        # Check for keywords in message text
        if message.text:
            text_lower = message.text.lower()
            
            # Check if any keyword is found
            found_keywords = []
            for keyword in self.keywords:
                if keyword.lower() in text_lower:
                    found_keywords.append(keyword)
            
            if found_keywords:
                await self.forward_message_to_owner(message, found_keywords, context)

    async def forward_message_to_owner(self, message, keywords, context):
        """Forward matching message to bot owner"""
        try:
            # Create notification message
            notification = f"""
🚨 **رسالة جديدة تحتوي على كلمات مفتاحية!**

👥 **المجموعة:** {message.chat.title or 'غير معروف'}
👤 **المرسل:** {message.from_user.first_name or 'غير معروف'}
🆔 **معرف المرسل:** @{message.from_user.username or 'لا يوجد'}
🔑 **الكلمات المفتاحية:** {', '.join(keywords)}
⏰ **الوقت:** {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}

📝 **الرسالة:**
{message.text}

---
💬 للرد على هذا الشخص: @{message.from_user.username or f"tg://user?id={message.from_user.id}"}
            """
            
            # Send notification to owner
            await context.bot.send_message(
                chat_id=self.owner_id,
                text=notification,
                parse_mode='Markdown'
            )
            
            logger.info(f"Forwarded message from {message.from_user.id} to owner")
            
        except Exception as e:
            logger.error(f"Error forwarding message: {e}")

async def main():
    """Main function to run the bot"""
    # Get token and owner ID from environment variables
    TOKEN = os.getenv('TELEGRAM_BOT_TOKEN')
    OWNER_ID = int(os.getenv('OWNER_ID', '0'))
    
    if not TOKEN:
        logger.error("TELEGRAM_BOT_TOKEN environment variable not set!")
        return
        
    if not OWNER_ID:
        logger.error("OWNER_ID environment variable not set!")
        return
    
    # Create bot instance
    bot = SaudiBot(TOKEN, OWNER_ID)
    
    # Create application
    application = Application.builder().token(TOKEN).build()
    
    # Add handlers
    application.add_handler(CommandHandler("start", bot.start))
    application.add_handler(CommandHandler("help", bot.help_command))
    application.add_handler(CommandHandler("keywords", bot.keywords_command))
    application.add_handler(CommandHandler("groups", bot.groups_command))
    application.add_handler(CommandHandler("stats", bot.stats_command))
    
    # Monitor all text messages
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, bot.monitor_messages))
    
    # Start the bot
    logger.info("Starting Saudi Bot on Railway...")
    
    # Use webhook for Railway deployment
    PORT = int(os.environ.get('PORT', 8080))
    await application.initialize()
    await application.start()
    await application.updater.start_webhook(
        listen="0.0.0.0",
        port=PORT,
        url_path=TOKEN,
        webhook_url=f"https://{os.environ.get('RAILWAY_STATIC_URL', 'localhost')}/{TOKEN}"
    )

if __name__ == '__main__':
    asyncio.run(main())
