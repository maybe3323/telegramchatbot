# Telegram AI Chat Assistant

An AI-powered Telegram bot that provides intelligent responses using free AI APIs.

## Features

- AI-powered conversations using free APIs
- Group chat support with mention detection
- Contextual responses based on chat type
- Easy configuration using environment variables
- Comprehensive logging system
- Error handling and recovery

## Setup

1. Clone this repository
2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
3. Set up environment variables:
   ```bash
   TELEGRAM_BOT_TOKEN=your_bot_token_here
   ```
4. Run the bot:
   ```bash
   python main.py
   ```

## Commands

- `/start` - Welcome message and bot introduction
- `/help` - Show help message
- `/status` - Display bot status and stats
- `/echo <message>` - Echo your message back
- `/reset` - Clear conversation history

## Configuration

The bot can be configured using environment variables:
- `TELEGRAM_BOT_TOKEN` - Your Telegram bot token (required)
- `DEBUG` - Enable debug mode (optional)
- `LOG_LEVEL` - Set logging level (optional, default: INFO)

## License

MIT License
