"""
Bot command and message handlers.
Contains all the logic for handling different types of user interactions.
"""

import logging
from datetime import datetime
from telegram import Update
from telegram.ext import ContextTypes
from utils import format_user_info, is_valid_message
from ai_service import AIService

logger = logging.getLogger(__name__)

class BotHandlers:
    """Class containing all bot message and command handlers."""
    
    def __init__(self):
        """Initialize handlers with any required state."""
        self.start_time = datetime.now()
        self.message_count = 0
        self.ai_service = AIService()
        self.group_message_count = 0
    
    async def start_command(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """
        Handle the /start command.
        
        Args:
            update: Telegram update object
            context: Bot context
        """
        try:
            user = update.effective_user
            user_info = format_user_info(user)
            
            chat_type = update.effective_chat.type if update.effective_chat else "private"
            is_group = chat_type in ['group', 'supergroup']
            
            if is_group:
                welcome_message = f"""
🤖 *Welcome to the AI-Enhanced Group Bot!*

Hello {user.first_name if user.first_name else 'there'}! 

I'm now active in this group and ready to participate in conversations!

*How to interact with me in groups:*
• Mention me with @{context.bot.username or 'botname'} to get my attention
• Reply to my messages to continue conversations
• Use commands like /help, /status anywhere

*Available Commands:*
• /start - Show this welcome message
• /help - Get help and available commands  
• /status - Check bot status and stats
• /echo <message> - Echo your message back
• /reset - Clear conversation history

I use AI to provide intelligent, contextual responses instead of repetitive messages!
                """
            else:
                welcome_message = f"""
🤖 *Welcome to the AI-Enhanced 24/7 Bot!*

Hello {user.first_name if user.first_name else 'there'}!

I'm your AI-powered bot that's available around the clock with intelligent responses.

*Available Commands:*
• /start - Show this welcome message
• /help - Get help and available commands
• /status - Check bot status
• /echo <message> - Echo your message back
• /reset - Clear conversation history

*New Features:*
• AI-powered conversations (no more repetitive responses!)
• Group chat support with mention detection
• Contextual responses based on chat type

Just send me any message and I'll respond intelligently!
                """
            
            await update.message.reply_text(
                welcome_message,
                parse_mode='Markdown'
            )
            
            logger.info(f"Start command received from {user_info}")
            
        except Exception as e:
            logger.error(f"Error in start_command: {e}")
            await update.message.reply_text(
                "Sorry, something went wrong. Please try again later."
            )
    
    async def help_command(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """
        Handle the /help command.
        
        Args:
            update: Telegram update object
            context: Bot context
        """
        try:
            chat_type = update.effective_chat.type if update.effective_chat else "private"
            is_group = chat_type in ['group', 'supergroup']
            
            if is_group:
                help_message = """
🆘 *AI Group Bot Help*

*Available Commands:*
🏁 `/start` - Welcome message and bot introduction
❓ `/help` - Show this help message
📊 `/status` - Display bot status and group stats
🔄 `/echo <message>` - Echo your message back
🔄 `/reset` - Clear conversation history

*Group Interaction:*
• Mention me (@botname) to get my attention
• Reply to my messages to continue conversations
• I respond with AI-generated contextual replies
• I won't spam - only respond when mentioned or replied to

*AI Features:*
• Intelligent, non-repetitive responses
• Group-aware conversation handling
• Context understanding and memory
• Free AI service (no API costs)

*Bot Status:* Online with AI ✅
                """
            else:
                help_message = """
🆘 *AI Bot Help & Commands*

*Available Commands:*
🏁 `/start` - Welcome message and bot introduction
❓ `/help` - Show this help message
📊 `/status` - Display bot status and AI stats
🔄 `/echo <message>` - Echo your message back
🔄 `/reset` - Clear conversation history

*AI Message Handling:*
Send me any text and I'll respond with intelligent, contextual replies using free AI services!

*Enhanced Features:*
• 24/7 availability with AI responses
• Intelligent conversation handling
• Group chat support with mentions
• Non-repetitive, contextual responses
• Error handling and comprehensive logging

*Bot Status:* Online with AI Enhancement ✅
                """
            
            await update.message.reply_text(
                help_message,
                parse_mode='Markdown'
            )
            
            user = update.effective_user
            logger.info(f"Help command received from {format_user_info(user)}")
            
        except Exception as e:
            logger.error(f"Error in help_command: {e}")
            await update.message.reply_text(
                "Sorry, I couldn't display the help message. Please try again."
            )
    
    async def status_command(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """
        Handle the /status command.
        
        Args:
            update: Telegram update object
            context: Bot context
        """
        try:
            uptime = datetime.now() - self.start_time
            uptime_str = str(uptime).split('.')[0]  # Remove microseconds
            
            ai_stats = self.ai_service.get_conversation_stats()
            status_message = f"""
📊 *Bot Status Report*

🟢 *Status:* Online and Running
⏰ *Uptime:* {uptime_str}
🕐 *Started:* {self.start_time.strftime('%Y-%m-%d %H:%M:%S')}
💬 *Messages Processed:* {self.message_count}
👥 *Group Messages:* {self.group_message_count}
🧠 *AI Conversations:* {ai_stats['active_conversations']}
🤖 *Bot Version:* 2.0.0 (AI Enhanced)

*System Info:*
• Polling: Active ✅
• AI Service: Online ✅
• Group Support: Enabled ✅
• Error Handling: Enabled ✅
• Logging: Active ✅

All systems operational! 🚀
            """
            
            await update.message.reply_text(
                status_message,
                parse_mode='Markdown'
            )
            
            user = update.effective_user
            logger.info(f"Status command received from {format_user_info(user)}")
            
        except Exception as e:
            logger.error(f"Error in status_command: {e}")
            await update.message.reply_text(
                "Sorry, I couldn't retrieve the status information."
            )
    
    async def echo_command(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """
        Handle the /echo command.
        
        Args:
            update: Telegram update object
            context: Bot context
        """
        try:
            # Get the message text after the command
            message_text = update.message.text
            command_parts = message_text.split(' ', 1)
            
            if len(command_parts) < 2:
                await update.message.reply_text(
                    "Usage: /echo <message>\n\nExample: /echo Hello World!"
                )
                return
            
            echo_text = command_parts[1]
            await update.message.reply_text(f"🔄 Echo: {echo_text}")
            
            user = update.effective_user
            logger.info(f"Echo command received from {format_user_info(user)}: {echo_text}")
            
        except Exception as e:
            logger.error(f"Error in echo_command: {e}")
            await update.message.reply_text(
                "Sorry, I couldn't echo your message. Please try again."
            )
    
    async def handle_message(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """
        Handle regular text messages.
        
        Args:
            update: Telegram update object
            context: Bot context
        """
        try:
            user = update.effective_user
            chat = update.effective_chat
            message = update.message
            
            if not user or not chat or not message or not message.text:
                return
                
            message_text = message.text
            
            # Validate message
            if not is_valid_message(message_text):
                await message.reply_text(
                    "I received your message, but it seems to be empty or invalid. Please try again!"
                )
                return
            
            # Check if this is a group chat
            chat_type = chat.type
            is_group = chat_type in ['group', 'supergroup']
            
            # In groups, only respond if mentioned or if it's a direct reply
            if is_group:
                bot_username = context.bot.username
                is_mentioned = f"@{bot_username}" in message_text if bot_username else False
                is_reply_to_bot = message.reply_to_message and message.reply_to_message.from_user.id == context.bot.id
                
                if not (is_mentioned or is_reply_to_bot):
                    # Don't respond to every message in groups unless mentioned
                    return
                
                # Remove mention from message for processing
                if is_mentioned and bot_username:
                    message_text = message_text.replace(f"@{bot_username}", "").strip()
                
                self.group_message_count += 1
            
            # Increment message counter
            self.message_count += 1
            
            # Generate AI response
            user_id = str(user.id)
            response = self.ai_service.generate_response(message_text, user_id, chat_type)
            
            await message.reply_text(response)
            
            chat_info = f"{chat_type} chat" if is_group else "private chat"
            logger.info(f"Message from {format_user_info(user)} in {chat_info}: {message_text[:50]}...")
            
        except Exception as e:
            logger.error(f"Error in handle_message: {e}")
            if update.message:
                await update.message.reply_text(
                    "Sorry, I encountered an error processing your message. Please try again!"
                )
    
    async def reset_command(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """
        Handle the /reset command to clear AI conversation history.
        
        Args:
            update: Telegram update object
            context: Bot context
        """
        try:
            user = update.effective_user
            if not user or not update.message:
                return
                
            user_id = str(user.id)
            self.ai_service.clear_conversation_history(user_id)
            
            await update.message.reply_text(
                "🔄 *Conversation Reset*\n\nYour conversation history has been cleared. I'll start fresh with our next chat!",
                parse_mode='Markdown'
            )
            
            logger.info(f"Reset command received from {format_user_info(user)}")
            
        except Exception as e:
            logger.error(f"Error in reset_command: {e}")
            if update.message:
                await update.message.reply_text(
                    "Sorry, I couldn't reset the conversation. Please try again."
                )

    async def error_handler(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """
        Handle errors that occur during bot operation.
        
        Args:
            update: Telegram update object
            context: Bot context
        """
        logger.error(f"Update {update} caused error {context.error}")
        
        # Try to send error message to user if possible
        if update and update.effective_message:
            try:
                await update.effective_message.reply_text(
                    "🚨 Sorry, an unexpected error occurred. The issue has been logged and I'll keep working normally!"
                )
            except Exception as e:
                logger.error(f"Failed to send error message to user: {e}")
