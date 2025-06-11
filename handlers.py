"""
Bot command and message handlers.
Contains all the logic for handling different types of user interactions.
"""

import logging
from datetime import datetime
from telegram import Update
from telegram.ext import ContextTypes
from utils import format_user_info, is_valid_message

logger = logging.getLogger(__name__)

class BotHandlers:
    """Class containing all bot message and command handlers."""
    
    def __init__(self):
        """Initialize handlers with any required state."""
        self.start_time = datetime.now()
        self.message_count = 0
    
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
            
            welcome_message = f"""
🤖 *Welcome to the 24/7 Bot!*

Hello {user.first_name}! 👋

I'm your friendly bot that's available around the clock to help you.

*Available Commands:*
• /start - Show this welcome message
• /help - Get help and available commands
• /status - Check bot status
• /echo <message> - Echo your message back

You can also just send me any message and I'll respond!

Type /help for more information.
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
            help_message = """
🆘 *Bot Help & Commands*

*Available Commands:*

🏁 `/start` - Welcome message and bot introduction
❓ `/help` - Show this help message
📊 `/status` - Display bot status and uptime
🔄 `/echo <message>` - Echo your message back

*Message Handling:*
You can send me any text message and I'll respond with a friendly reply!

*Bot Features:*
• 24/7 availability
• Basic conversation handling
• Command processing
• Error handling and logging

*Need more help?*
This bot is designed to be simple and user-friendly. Just start chatting!

*Bot Status:* Online ✅
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
            
            status_message = f"""
📊 *Bot Status Report*

🟢 *Status:* Online and Running
⏰ *Uptime:* {uptime_str}
🕐 *Started:* {self.start_time.strftime('%Y-%m-%d %H:%M:%S')}
💬 *Messages Processed:* {self.message_count}
🤖 *Bot Version:* 1.0.0

*System Info:*
• Polling: Active ✅
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
            message_text = update.message.text
            
            # Validate message
            if not is_valid_message(message_text):
                await update.message.reply_text(
                    "I received your message, but it seems to be empty or invalid. Please try again!"
                )
                return
            
            # Increment message counter
            self.message_count += 1
            
            # Generate response based on message content
            response = self.generate_response(message_text)
            
            await update.message.reply_text(response)
            
            logger.info(f"Message from {format_user_info(user)}: {message_text[:50]}...")
            
        except Exception as e:
            logger.error(f"Error in handle_message: {e}")
            await update.message.reply_text(
                "Sorry, I encountered an error processing your message. Please try again!"
            )
    
    def generate_response(self, message_text: str) -> str:
        """
        Generate a response to user messages.
        
        Args:
            message_text: The user's message text
            
        Returns:
            Generated response string
        """
        message_lower = message_text.lower()
        
        # Greeting responses
        if any(greeting in message_lower for greeting in ['hello', 'hi', 'hey', 'good morning', 'good afternoon', 'good evening']):
            return "Hello there! 👋 How can I help you today? Feel free to use /help to see what I can do!"
        
        # Question responses
        elif '?' in message_text:
            return f"That's an interesting question! 🤔 While I'm a simple bot, I received your question: \"{message_text}\". Try using /help to see my available commands!"
        
        # Thanks responses
        elif any(thanks in message_lower for thanks in ['thank', 'thanks', 'appreciate']):
            return "You're very welcome! 😊 I'm here 24/7 if you need anything else!"
        
        # Bot-related queries
        elif any(word in message_lower for word in ['bot', 'robot', 'ai', 'artificial']):
            return "Yes, I'm a Telegram bot! 🤖 I'm designed to be helpful and available 24/7. Use /status to see how I'm doing!"
        
        # Help requests
        elif any(word in message_lower for word in ['help', 'assist', 'support']):
            return "I'd be happy to help! 🆘 Use /help to see all my available commands, or just keep chatting with me!"
        
        # Default response
        else:
            return f"Thanks for your message! 💬 I received: \"{message_text}\"\n\nI'm a simple bot, but I'm always here to chat! Use /help to see what commands I support."
    
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
