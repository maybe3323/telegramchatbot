"""
Main bot class that handles Telegram bot initialization and setup.
"""

import logging
from telegram.ext import Application, CommandHandler, MessageHandler, filters
from handlers import BotHandlers
from config import Config

logger = logging.getLogger(__name__)

class TelegramBot:
    """Main Telegram bot class."""
    
    def __init__(self, config: Config):
        """
        Initialize the Telegram bot.
        
        Args:
            config: Configuration object containing bot settings
        """
        self.config = config
        self.handlers = BotHandlers()
        self.application = None
        
    def setup_handlers(self):
        """Set up all bot command and message handlers."""
        # Command handlers
        self.application.add_handler(CommandHandler("start", self.handlers.start_command))
        self.application.add_handler(CommandHandler("help", self.handlers.help_command))
        self.application.add_handler(CommandHandler("status", self.handlers.status_command))
        self.application.add_handler(CommandHandler("echo", self.handlers.echo_command))
        self.application.add_handler(CommandHandler("reset", self.handlers.reset_command))
        
        # Message handlers
        self.application.add_handler(MessageHandler(
            filters.TEXT & ~filters.COMMAND, 
            self.handlers.handle_message
        ))
        
        # Error handler
        self.application.add_error_handler(self.handlers.error_handler)
        
        logger.info("All handlers have been set up successfully.")
    
    def start(self):
        """Start the bot with polling mechanism."""
        try:
            # Create application
            self.application = Application.builder().token(self.config.bot_token).build()
            
            # Set up handlers
            self.setup_handlers()
            
            logger.info("Bot initialized successfully. Starting polling...")
            
            # Start polling
            self.application.run_polling(
                poll_interval=1.0,
                timeout=10,
                bootstrap_retries=5,
                read_timeout=10,
                write_timeout=10,
                connect_timeout=10,
                pool_timeout=10
            )
            
        except Exception as e:
            logger.error(f"Failed to start bot: {e}")
            raise
