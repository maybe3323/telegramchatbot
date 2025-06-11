"""
Utility functions for the Telegram bot.
Contains helper functions used across different modules.
"""

import logging
import re
from typing import Optional
from telegram import User

logger = logging.getLogger(__name__)

def format_user_info(user: User) -> str:
    """
    Format user information for logging.
    
    Args:
        user: Telegram User object
        
    Returns:
        Formatted string with user information
    """
    if not user:
        return "Unknown User"
    
    info_parts = []
    
    # Add user ID
    if user.id:
        info_parts.append(f"ID:{user.id}")
    
    # Add username if available
    if user.username:
        info_parts.append(f"@{user.username}")
    
    # Add first name
    if user.first_name:
        info_parts.append(f"Name:{user.first_name}")
        
        # Add last name if available
        if user.last_name:
            info_parts[-1] += f" {user.last_name}"
    
    return " | ".join(info_parts) if info_parts else "Unknown User"

def is_valid_message(message_text: Optional[str]) -> bool:
    """
    Validate if a message text is valid and not empty.
    
    Args:
        message_text: The message text to validate
        
    Returns:
        Boolean indicating if the message is valid
    """
    if not message_text:
        return False
    
    # Check if message is not just whitespace
    if not message_text.strip():
        return False
    
    # Check for reasonable length (not too long)
    if len(message_text) > 4096:  # Telegram's message limit
        logger.warning(f"Message too long: {len(message_text)} characters")
        return False
    
    return True

def sanitize_text(text: str) -> str:
    """
    Sanitize text for safe display and logging.
    
    Args:
        text: Text to sanitize
        
    Returns:
        Sanitized text string
    """
    if not text:
        return ""
    
    # Remove or replace potentially problematic characters
    # Keep basic punctuation and alphanumeric characters
    sanitized = re.sub(r'[^\w\s\.\,\!\?\-\:\;\(\)\[\]\'\"]+', '', text)
    
    # Limit length for logging
    if len(sanitized) > 200:
        sanitized = sanitized[:197] + "..."
    
    return sanitized.strip()

def get_command_from_message(message_text: str) -> Optional[str]:
    """
    Extract command from message text.
    
    Args:
        message_text: Full message text
        
    Returns:
        Command string without '/' or None if not a command
    """
    if not message_text or not message_text.startswith('/'):
        return None
    
    # Split and get first word
    parts = message_text.split()
    if not parts:
        return None
    
    command = parts[0][1:]  # Remove '/' prefix
    
    # Handle commands with @botname
    if '@' in command:
        command = command.split('@')[0]
    
    return command.lower()

def format_uptime(start_time, current_time) -> str:
    """
    Format uptime duration into human-readable string.
    
    Args:
        start_time: Bot start time
        current_time: Current time
        
    Returns:
        Formatted uptime string
    """
    uptime_delta = current_time - start_time
    
    days = uptime_delta.days
    hours, remainder = divmod(uptime_delta.seconds, 3600)
    minutes, seconds = divmod(remainder, 60)
    
    parts = []
    
    if days > 0:
        parts.append(f"{days} day{'s' if days != 1 else ''}")
    
    if hours > 0:
        parts.append(f"{hours} hour{'s' if hours != 1 else ''}")
    
    if minutes > 0:
        parts.append(f"{minutes} minute{'s' if minutes != 1 else ''}")
    
    if seconds > 0 and not parts:  # Only show seconds if no larger units
        parts.append(f"{seconds} second{'s' if seconds != 1 else ''}")
    
    return ", ".join(parts) if parts else "Less than a minute"

def log_bot_event(event_type: str, user_info: str, details: str = ""):
    """
    Log bot events in a standardized format.
    
    Args:
        event_type: Type of event (command, message, error, etc.)
        user_info: Formatted user information
        details: Additional event details
    """
    log_message = f"[{event_type.upper()}] {user_info}"
    
    if details:
        log_message += f" - {details}"
    
    logger.info(log_message)

def is_bot_command(message_text: str) -> bool:
    """
    Check if message text is a bot command.
    
    Args:
        message_text: Message text to check
        
    Returns:
        Boolean indicating if it's a command
    """
    return bool(message_text and message_text.strip().startswith('/'))
