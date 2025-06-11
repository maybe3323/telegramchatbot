"""
Configuration management for the Telegram bot.
Handles environment variables and bot settings.
"""

import os
import logging

logger = logging.getLogger(__name__)

class Config:
    """Configuration class for bot settings."""
    
    def __init__(self):
        """Initialize configuration from environment variables."""
        self.bot_token = self._get_bot_token()
        self.debug_mode = self._get_debug_mode()
        self.log_level = self._get_log_level()
        
        # Validate required configuration
        self._validate_config()
    
    def _get_bot_token(self) -> str:
        """
        Get bot token from environment variables.
        
        Returns:
            Bot token string or empty string if not found
        """
        token = os.getenv('TELEGRAM_BOT_TOKEN', '').strip()
        
        if not token:
            # Try alternative environment variable names
            token = os.getenv('BOT_TOKEN', '').strip()
        
        if token:
            logger.info("Bot token loaded successfully from environment variables.")
        else:
            logger.error("Bot token not found in environment variables.")
        
        return token
    
    def _get_debug_mode(self) -> bool:
        """
        Get debug mode setting from environment variables.
        
        Returns:
            Boolean indicating if debug mode is enabled
        """
        debug = os.getenv('DEBUG', 'false').lower()
        return debug in ['true', '1', 'yes', 'on']
    
    def _get_log_level(self) -> str:
        """
        Get logging level from environment variables.
        
        Returns:
            Log level string (default: INFO)
        """
        level = os.getenv('LOG_LEVEL', 'INFO').upper()
        valid_levels = ['DEBUG', 'INFO', 'WARNING', 'ERROR', 'CRITICAL']
        
        if level not in valid_levels:
            logger.warning(f"Invalid log level '{level}', using INFO instead.")
            return 'INFO'
        
        return level
    
    def _validate_config(self):
        """Validate that all required configuration is present."""
        if not self.bot_token:
            raise ValueError(
                "Bot token is required. Please set the TELEGRAM_BOT_TOKEN environment variable."
            )
        
        # Basic token format validation
        if not self.bot_token.count(':') == 1:
            logger.warning("Bot token format appears to be invalid. Expected format: 'bot_id:token'")
    
    def get_config_summary(self) -> dict:
        """
        Get a summary of current configuration (without sensitive data).
        
        Returns:
            Dictionary with configuration summary
        """
        return {
            'bot_token_present': bool(self.bot_token),
            'bot_token_length': len(self.bot_token) if self.bot_token else 0,
            'debug_mode': self.debug_mode,
            'log_level': self.log_level
        }
