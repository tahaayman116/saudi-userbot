#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Telegram Bot for Monitoring Group Messages
Monitors groups for specific Arabic keywords and forwards relevant messages
"""

import os
import logging
import json
from datetime import datetime
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes, CallbackQueryHandler
import re

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
        self.load_config()
        
    def load_config(self):
        """Load configuration from file"""
        try:
            if os.path.exists('config.json'):
                with open('config.json', 'r', encoding='utf-8') as f:
                    config = json.load(f)
                    self.keywords = config.get('keywords', self.keywords)
                    self.monitored_groups = set(config.get('monitored_groups', []))
        except Exception as e:
            logger.error(f"Error loading config: {e}")
    
    def save_config(self):
        """Save configuration to file"""
        try:
            config = {
                'keywords': self.keywords,
                'monitored_groups': list(self.monitored_groups)
            }
            with open('config.json', 'w', encoding='utf-8') as f:
                json.dump(config, f, ensure_ascii=False, indent=2)
        except Exception as e:
            logger.error(f"Error saving config: {e}")

    async def start(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Handle /start command"""
        user_id = update.effective_user.id
        
        if user_id == self.owner_id:
            welcome_text = """
🤖 مرحباً بك في بوت مراقبة المجموعات!

الأوامر المتاحة:
/keywords - عرض وتعديل الكلمات المفتاحية
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
/keywords - إدارة الكلمات المفتاحية
/groups - عرض المجموعات المراقبة
/stats - عرض الإحصائيات

💡 **نصائح:**
- تأكد من إعطاء البوت صلاحية قراءة الرسائل
- يمكنك إضافة كلمات مفتاحية جديدة في أي وقت
- البوت يعمل مع النصوص العربية والإنجليزية
        """
        await update.message.reply_text(help_text)

    async def keywords_command(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Handle /keywords command"""
        if update.effective_user.id != self.owner_id:
            return
            
        keyboard = [
            [InlineKeyboardButton("عرض الكلمات المفتاحية", callback_data="show_keywords")],
            [InlineKeyboardButton("إضافة كلمة جديدة", callback_data="add_keyword")],
            [InlineKeyboardButton("حذف كلمة", callback_data="delete_keyword")]
        ]
        reply_markup = InlineKeyboardMarkup(keyboard)
        
        await update.message.reply_text(
            "🔑 إدارة الكلمات المفتاحية:",
            reply_markup=reply_markup
        )

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

    async def button_handler(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Handle inline keyboard buttons"""
        query = update.callback_query
        await query.answer()
        
        if query.data == "show_keywords":
            keywords_text = "🔑 الكلمات المفتاحية الحالية:\n\n"
            for i, keyword in enumerate(self.keywords, 1):
                keywords_text += f"{i}. {keyword}\n"
            await query.edit_message_text(keywords_text)
            
        elif query.data == "add_keyword":
            await query.edit_message_text(
                "📝 لإضافة كلمة مفتاحية جديدة، أرسل:\n"
                "/add_keyword الكلمة_الجديدة"
            )
            
        elif query.data == "delete_keyword":
            await query.edit_message_text(
                "🗑️ لحذف كلمة مفتاحية، أرسل:\n"
                "/delete_keyword الكلمة_المراد_حذفها"
            )

    async def add_keyword_command(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Add new keyword"""
        if update.effective_user.id != self.owner_id:
            return
            
        if not context.args:
            await update.message.reply_text("❌ يرجى إدخال الكلمة المفتاحية")
            return
            
        keyword = ' '.join(context.args)
        if keyword not in self.keywords:
            self.keywords.append(keyword)
            self.save_config()
            await update.message.reply_text(f"✅ تم إضافة الكلمة المفتاحية: {keyword}")
        else:
            await update.message.reply_text(f"⚠️ الكلمة المفتاحية موجودة بالفعل: {keyword}")

    async def delete_keyword_command(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Delete keyword"""
        if update.effective_user.id != self.owner_id:
            return
            
        if not context.args:
            await update.message.reply_text("❌ يرجى إدخال الكلمة المفتاحية المراد حذفها")
            return
            
        keyword = ' '.join(context.args)
        if keyword in self.keywords:
            self.keywords.remove(keyword)
            self.save_config()
            await update.message.reply_text(f"✅ تم حذف الكلمة المفتاحية: {keyword}")
        else:
            await update.message.reply_text(f"❌ الكلمة المفتاحية غير موجودة: {keyword}")

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
        if group_id not in self.monitored_groups:
            self.monitored_groups.add(group_id)
            self.save_config()
            
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

def main():
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
    application.add_handler(CommandHandler("add_keyword", bot.add_keyword_command))
    application.add_handler(CommandHandler("delete_keyword", bot.delete_keyword_command))
    application.add_handler(CallbackQueryHandler(bot.button_handler))
    
    # Monitor all text messages
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, bot.monitor_messages))
    
    # Start the bot
    logger.info("Starting Saudi Bot...")
    application.run_polling(allowed_updates=Update.ALL_TYPES)

if __name__ == '__main__':
    main()
