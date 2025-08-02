import json
from channels.generic.websocket import AsyncWebsocketConsumer
from channels.db import database_sync_to_async
from django.contrib.auth.models import User
from .models import ChatMessage
import uuid

class ChatConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.session_id = str(uuid.uuid4())
        self.room_group_name = f"chat_{self.session_id}"

        # Join room group
        await self.channel_layer.group_add(
            self.room_group_name,
            self.channel_name
        )

        await self.accept()

        # Send welcome message
        await self.send(text_data=json.dumps({
            'type': 'chat_message',
            'message': "Hello! I'm your healthcare assistant. How can I help you today?",
            'sender': 'bot',
            'session_id': self.session_id
        }))

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

        # Save user message to database
        if user_id:
            await self.save_message(user_id, message, 'USER', self.session_id)

        # Generate bot response
        bot_response = await self.generate_bot_response(message)

        # Save bot response to database
        if user_id:
            await self.save_message(user_id, bot_response, 'BOT', self.session_id)

        # Send message to room group
        await self.channel_layer.group_send(
            self.room_group_name,
            {
                'type': 'chat_message',
                'message': message,
                'sender': 'user',
                'session_id': self.session_id
            }
        )

        # Send bot response
        await self.channel_layer.group_send(
            self.room_group_name,
            {
                'type': 'chat_message',
                'message': bot_response,
                'sender': 'bot',
                'session_id': self.session_id
            }
        )

    # Receive message from room group
    async def chat_message(self, event):
        message = event['message']
        sender = event['sender']
        session_id = event['session_id']

        # Send message to WebSocket
        await self.send(text_data=json.dumps({
            'message': message,
            'sender': sender,
            'session_id': session_id
        }))

    @database_sync_to_async
    def save_message(self, user_id, content, message_type, session_id):
        try:
            user = User.objects.get(id=user_id)
            ChatMessage.objects.create(
                session_id=session_id,
                message_type=message_type,
                content=content,
                user=user
            )
        except User.DoesNotExist:
            pass

    @database_sync_to_async
    def generate_bot_response(self, message):
        message_lower = message.lower()
        
        # Simple response logic (in real app, use NLP/AI)
        if any(word in message_lower for word in ['hello', 'hi', 'hey']):
            return "Hello! I'm your healthcare assistant. How can I help you today?"
        elif any(word in message_lower for word in ['symptom', 'pain', 'hurt', 'ache']):
            return "I can help you check your symptoms. Please visit our symptom checker page for a detailed analysis. What symptoms are you experiencing?"
        elif any(word in message_lower for word in ['medicine', 'drug', 'medication', 'pill']):
            return "I can help you find medicines. Please visit our pharmacy section to browse available medications. What type of medicine are you looking for?"
        elif any(word in message_lower for word in ['appointment', 'doctor', 'visit', 'consultation']):
            return "For appointments, please contact our support team or visit a nearby healthcare facility. Would you like me to help you find a doctor?"
        elif any(word in message_lower for word in ['fever', 'temperature']):
            return "Fever can be a sign of various conditions. Please monitor your temperature and consider consulting a doctor if it persists. Are you experiencing any other symptoms?"
        elif any(word in message_lower for word in ['headache', 'migraine']):
            return "Headaches can have many causes. Try resting in a quiet, dark room and staying hydrated. If severe or persistent, please consult a doctor."
        elif any(word in message_lower for word in ['cough', 'cold', 'flu']):
            return "For cough and cold symptoms, rest, stay hydrated, and consider over-the-counter medications. If symptoms persist, see a doctor."
        elif any(word in message_lower for word in ['thank', 'thanks']):
            return "You're welcome! I'm here to help with your healthcare needs. Is there anything else you'd like to know?"
        elif any(word in message_lower for word in ['bye', 'goodbye', 'exit']):
            return "Thank you for using our healthcare assistant. Take care and stay healthy!"
        else:
            return "I'm here to help with your healthcare needs. You can ask me about symptoms, medicines, appointments, or general health questions. What would you like to know?"