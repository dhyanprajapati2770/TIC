import json
from channels.generic.websocket import AsyncWebsocketConsumer
from channels.db import database_sync_to_async
from django.contrib.auth import get_user_model
from .models import ChatSession, ChatMessage, BotResponse
import uuid

User = get_user_model()


class ChatConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.session_id = self.scope['url_route']['kwargs']['session_id']
        self.room_group_name = f'chat_{self.session_id}'

        # Join room group
        await self.channel_layer.group_add(
            self.room_group_name,
            self.channel_name
        )

        await self.accept()

    async def disconnect(self, close_code):
        # Leave room group
        await self.channel_layer.group_discard(
            self.room_group_name,
            self.channel_name
        )

    # Receive message from WebSocket
    async def receive(self, text_data):
        text_data_json = json.loads(text_data)
        message = text_data_json['message']
        user_id = text_data_json.get('user_id')

        # Save user message
        await self.save_message(user_id, message, 'user')

        # Generate bot response
        bot_response = await self.generate_bot_response(message)

        # Save bot response
        await self.save_message(user_id, bot_response, 'bot')

        # Send message to room group
        await self.channel_layer.group_send(
            self.room_group_name,
            {
                'type': 'chat_message',
                'message': message,
                'user_id': user_id,
                'message_type': 'user'
            }
        )

        # Send bot response to room group
        await self.channel_layer.group_send(
            self.room_group_name,
            {
                'type': 'chat_message',
                'message': bot_response,
                'user_id': None,
                'message_type': 'bot'
            }
        )

    # Receive message from room group
    async def chat_message(self, event):
        message = event['message']
        user_id = event['user_id']
        message_type = event['message_type']

        # Send message to WebSocket
        await self.send(text_data=json.dumps({
            'message': message,
            'user_id': user_id,
            'message_type': message_type
        }))

    @database_sync_to_async
    def save_message(self, user_id, content, message_type):
        """Save message to database."""
        try:
            user = User.objects.get(id=user_id) if user_id else None
            session, created = ChatSession.objects.get_or_create(
                session_id=self.session_id,
                defaults={'user': user}
            )
            
            ChatMessage.objects.create(
                session=session,
                message_type=message_type,
                content=content
            )
        except Exception as e:
            print(f"Error saving message: {e}")

    @database_sync_to_async
    def generate_bot_response(self, user_message):
        """Generate bot response based on user message."""
        try:
            # Simple keyword-based response system
            user_message_lower = user_message.lower()
            
            # Get all active bot responses
            responses = BotResponse.objects.filter(is_active=True).order_by('-priority')
            
            for response in responses:
                keywords = [kw.strip().lower() for kw in response.trigger_keywords.split(',')]
                if any(keyword in user_message_lower for keyword in keywords):
                    return response.response_text
            
            # Default response if no keywords match
            default_responses = [
                "I'm here to help you with your health concerns. Could you please provide more details about your symptoms?",
                "I understand you're not feeling well. Can you describe your symptoms so I can better assist you?",
                "I'm your virtual health assistant. Please let me know what health-related questions you have.",
                "I'm here to help with symptom checking, medicine information, and general health advice. What would you like to know?"
            ]
            
            import random
            return random.choice(default_responses)
            
        except Exception as e:
            print(f"Error generating bot response: {e}")
            return "I'm sorry, I'm having trouble processing your request. Please try again."