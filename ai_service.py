"""
AI service module for generating intelligent responses using free APIs.
Uses Hugging Face's free Inference API for natural language generation.
"""

import requests
import json
import logging
import random
from typing import Optional

logger = logging.getLogger(__name__)

class AIService:
    """Service for generating AI-powered responses using free APIs."""
    
    def __init__(self):
        """Initialize the AI service with free API endpoints."""
        # Multiple free endpoints for redundancy
        self.endpoints = [
            "https://api-inference.huggingface.co/models/microsoft/DialoGPT-medium",
            "https://api-inference.huggingface.co/models/facebook/blenderbot-400M-distill",
            "https://api-inference.huggingface.co/models/microsoft/DialoGPT-small"
        ]
        self.current_endpoint = 0
        self.conversation_history = {}
        
    def generate_response(self, message: str, user_id: str, chat_type: str = "private") -> str:
        """
        Generate an AI response to a user message.
        
        Args:
            message: User's message
            user_id: Unique identifier for the user
            chat_type: Type of chat (private, group, supergroup)
            
        Returns:
            Generated response string
        """
        try:
            # Try different approaches for better responses
            response = self._try_huggingface_api(message, user_id)
            
            if response:
                return response
            else:
                # Fallback to enhanced rule-based responses
                return self._generate_smart_fallback(message, chat_type)
                
        except Exception as e:
            logger.error(f"Error generating AI response: {e}")
            return self._generate_smart_fallback(message, chat_type)
    
    def _try_huggingface_api(self, message: str, user_id: str) -> Optional[str]:
        """Try to get response from Hugging Face API."""
        try:
            # Use the current endpoint
            endpoint = self.endpoints[self.current_endpoint]
            
            headers = {
                "Content-Type": "application/json",
            }
            
            # Prepare the payload
            if "DialoGPT" in endpoint:
                # For DialoGPT, use conversation format
                conversation = self.conversation_history.get(user_id, [])
                conversation.append(message)
                
                payload = {
                    "inputs": {
                        "past_user_inputs": conversation[:-1] if len(conversation) > 1 else [],
                        "generated_responses": [],
                        "text": message
                    }
                }
            else:
                # For other models, use simple text input
                payload = {
                    "inputs": message,
                    "parameters": {
                        "max_length": 100,
                        "temperature": 0.7,
                        "do_sample": True
                    }
                }
            
            # Make the request with a short timeout
            response = requests.post(
                endpoint,
                headers=headers,
                json=payload,
                timeout=5
            )
            
            if response.status_code == 200:
                result = response.json()
                
                if isinstance(result, list) and len(result) > 0:
                    if "generated_text" in result[0]:
                        generated_text = result[0]["generated_text"]
                        # Clean up the response
                        if isinstance(generated_text, str):
                            # Remove the original input from response
                            if message in generated_text:
                                generated_text = generated_text.replace(message, "").strip()
                            return generated_text[:200] if generated_text else None
                elif isinstance(result, dict) and "generated_text" in result:
                    return result["generated_text"][:200]
                    
            # If this endpoint fails, try the next one
            self.current_endpoint = (self.current_endpoint + 1) % len(self.endpoints)
            return None
            
        except Exception as e:
            logger.warning(f"Hugging Face API failed: {e}")
            return None
    
    def _generate_smart_fallback(self, message: str, chat_type: str) -> str:
        """Generate intelligent fallback responses without repetition."""
        message_lower = message.lower()
        
        # Context-aware responses for groups vs private chats
        if chat_type in ["group", "supergroup"]:
            responses = self._get_group_responses(message_lower)
        else:
            responses = self._get_private_responses(message_lower)
        
        # Add some randomness to avoid repetition
        return random.choice(responses)
    
    def _get_group_responses(self, message_lower: str) -> list:
        """Get appropriate responses for group chats."""
        
        # Greeting responses for groups
        if any(greeting in message_lower for greeting in ['hello', 'hi', 'hey', 'good morning', 'good afternoon', 'good evening']):
            return [
                "Hey everyone! How's it going?",
                "Hello there! Great to see some activity in the group!",
                "Hi! Hope everyone's having a good day!",
                "Greetings! What's the discussion about today?",
                "Hey! Good to see you all here!"
            ]
        
        # Question responses for groups
        elif '?' in message_lower:
            return [
                "That's an interesting question! Anyone else have thoughts on this?",
                "Good question! I'd love to hear what others think too.",
                "Hmm, that's worth discussing. What do you all think?",
                "Interesting point! Does anyone have experience with this?",
                "Great question for the group! Let's see what everyone thinks."
            ]
        
        # Thanks responses for groups
        elif any(thanks in message_lower for thanks in ['thank', 'thanks', 'appreciate']):
            return [
                "You're welcome! Happy to help the group!",
                "No problem! That's what this community is for!",
                "Glad I could contribute to the discussion!",
                "Anytime! Love seeing helpful conversations here!",
                "You're very welcome! Keep the great discussions going!"
            ]
        
        # Bot-related queries for groups
        elif any(word in message_lower for word in ['bot', 'robot', 'ai']):
            return [
                "Yes, I'm your friendly group bot! Here to help keep conversations interesting!",
                "That's me! I'm here to assist and engage with the group!",
                "Correct! I'm an AI bot designed to make group chats more interactive!",
                "Indeed! I'm here to contribute to your group discussions!",
                "Yep! Your resident bot, ready to chat and help out!"
            ]
        
        # Help requests for groups
        elif any(word in message_lower for word in ['help', 'assist', 'support']):
            return [
                "I'm here to help! What can I assist the group with?",
                "Happy to help out! What do you need assistance with?",
                "Sure thing! How can I support the group today?",
                "Of course! I'm here to make things easier for everyone!",
                "Absolutely! What kind of help are you looking for?"
            ]
        
        # Default group responses
        else:
            return [
                f"Interesting point about '{message_lower[:30]}...' - what does everyone else think?",
                "That's a cool topic! Anyone else want to share their thoughts?",
                "Thanks for sharing! I find group discussions really engaging.",
                "Good point! This group always has such thoughtful conversations.",
                "I appreciate you bringing this up - it's great to see active discussions!",
                "That's worth discussing further! What are your experiences with this?",
                "Interesting perspective! I'd love to hear more viewpoints from the group."
            ]
    
    def _get_private_responses(self, message_lower: str) -> list:
        """Get appropriate responses for private chats."""
        
        # Greeting responses for private chats
        if any(greeting in message_lower for greeting in ['hello', 'hi', 'hey', 'good morning', 'good afternoon', 'good evening']):
            return [
                "Hello! Nice to chat with you personally. How can I help?",
                "Hi there! Great to have a one-on-one conversation. What's on your mind?",
                "Hey! I'm all ears. What would you like to talk about?",
                "Good to see you! How has your day been going?",
                "Hello! I'm here and ready to chat. What's new with you?"
            ]
        
        # Question responses for private chats
        elif '?' in message_lower:
            return [
                f"That's a thoughtful question about '{message_lower[:30]}...' Let me think about that!",
                "You've got me curious now! That's definitely something worth exploring.",
                "Great question! I find these kinds of topics really engaging.",
                "That's an interesting way to look at it. What made you think of that?",
                "I love questions like this! They really make you think, don't they?"
            ]
        
        # Thanks responses for private chats
        elif any(thanks in message_lower for thanks in ['thank', 'thanks', 'appreciate']):
            return [
                "You're absolutely welcome! I really enjoy our conversations.",
                "My pleasure! I'm always happy to chat with you.",
                "Don't mention it! These discussions are great.",
                "Anytime! I appreciate you taking the time to chat.",
                "You're very welcome! Feel free to reach out whenever you want to talk."
            ]
        
        # Bot-related queries for private chats
        elif any(word in message_lower for word in ['bot', 'robot', 'ai']):
            return [
                "Yes, I'm an AI bot, but I try to make our conversations feel natural and engaging!",
                "That's right! I'm here to be your personal chat companion whenever you need one.",
                "Indeed I am! But I like to think of myself as a friendly conversation partner.",
                "Correct! I'm designed to have meaningful conversations just like this one.",
                "Yes, but don't let that stop us from having great chats together!"
            ]
        
        # Help requests for private chats
        elif any(word in message_lower for word in ['help', 'assist', 'support']):
            return [
                "I'd be delighted to help! What's on your mind?",
                "Absolutely! I'm here to assist however I can. What do you need?",
                "Of course! I love being helpful. How can I support you today?",
                "I'm all yours! What kind of assistance are you looking for?",
                "Happy to help! Just let me know what you'd like to discuss or work on."
            ]
        
        # Default private responses
        else:
            return [
                f"That's really interesting what you said about '{message_lower[:30]}...' Tell me more!",
                "I find that fascinating! What's your experience been with that?",
                "You've got me thinking now. That's a really good point you make.",
                "I appreciate you sharing that with me. What led you to that conclusion?",
                "That's a unique perspective! I'd love to hear more of your thoughts on it.",
                "Thanks for bringing that up - it's given me something new to consider!",
                "I really enjoy these kinds of conversations with you. What else is on your mind?"
            ]
    
    def clear_conversation_history(self, user_id: str):
        """Clear conversation history for a user."""
        if user_id in self.conversation_history:
            del self.conversation_history[user_id]
    
    def get_conversation_stats(self) -> dict:
        """Get statistics about conversations."""
        return {
            "active_conversations": len(self.conversation_history),
            "current_endpoint": self.endpoints[self.current_endpoint],
            "total_endpoints": len(self.endpoints)
        }