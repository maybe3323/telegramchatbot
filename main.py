#!/usr/bin/env python3
"""
Main entry point for the Telegram bot.
Handles bot initialization and starts the polling loop.
"""

import logging
import sys
from bot import TelegramBot
from config import Config
from keep_alive import keep_alive

# Configure logging
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO,
    handlers=[
        logging.FileHandler('bot.log'),
        logging.StreamHandler(sys.stdout)
    ]
)

logger = logging.getLogger(__name__)

def main():
    """Main function to start the Telegram bot."""
    try:
        # Start keep_alive web server (for Replit/UptimeRobot)
        keep_alive()

        # Initialize configuration
        config = Config()
        
        # Validate bot token
        if not config.bot_token:
            logger.error("Bot token not found. Please set the TELEGRAM_BOT_TOKEN environment variable.")
            sys.exit(1)
        
        # Initialize and start the bot
        bot = TelegramBot(config)
        logger.info("Starting Telegram bot...")
        bot.start()
        
    except KeyboardInterrupt:
        logger.info("Bot stopped by user.")
    except Exception as e:
        logger.error(f"Fatal error occurred: {e}")
        sys.exit(1)

if __name__ == '__main__':
    main()
