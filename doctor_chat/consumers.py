import json
from channels.generic.websocket import AsyncWebsocketConsumer
from channels.db import database_sync_to_async
from django.contrib.auth import get_user_model
from .models import ChatRoom, Message
import logging

logger = logging.getLogger('healthcare')
User = get_user_model()


class ChatConsumer(AsyncWebsocketConsumer):
    """WebSocket consumer for general chat rooms"""
    
    async def connect(self):
        self.room_name = self.scope['url_route']['kwargs']['room_name']
        self.room_group_name = f'chat_{self.room_name}'
        
        # Join room group
        await self.channel_layer.group_add(
            self.room_group_name,
            self.channel_name
        )
        
        await self.accept()
        logger.info(f"User connected to chat room: {self.room_name}")
    
    async def disconnect(self, close_code):
        # Leave room group
        await self.channel_layer.group_discard(
            self.room_group_name,
            self.channel_name
        )
        logger.info(f"User disconnected from chat room: {self.room_name}")
    
    async def receive(self, text_data):
        try:
            text_data_json = json.loads(text_data)
            message = text_data_json['message']
            username = text_data_json.get('username', 'Anonymous')
            message_type = text_data_json.get('type', 'chat_message')
            
            # Save message to database
            await self.save_message(self.room_name, username, message)
            
            # Send message to room group
            await self.channel_layer.group_send(
                self.room_group_name,
                {
                    'type': 'chat_message',
                    'message': message,
                    'username': username,
                    'timestamp': text_data_json.get('timestamp')
                }
            )
        except Exception as e:
            logger.error(f"Error in chat receive: {e}")
    
    async def chat_message(self, event):
        # Send message to WebSocket
        await self.send(text_data=json.dumps({
            'type': 'chat_message',
            'message': event['message'],
            'username': event['username'],
            'timestamp': event.get('timestamp')
        }))
    
    @database_sync_to_async
    def save_message(self, room_name, username, message):
        try:
            # Get or create chat room
            room, created = ChatRoom.objects.get_or_create(name=room_name)
            
            # Get user (if authenticated)
            user = None
            try:
                user = User.objects.get(username=username)
            except User.DoesNotExist:
                pass
            
            # Save message
            Message.objects.create(
                room=room,
                user=user,
                content=message
            )
        except Exception as e:
            logger.error(f"Error saving message: {e}")


class DoctorChatConsumer(AsyncWebsocketConsumer):
    """WebSocket consumer for doctor-patient consultations"""
    
    async def connect(self):
        self.user = self.scope["user"]
        
        if not self.user.is_authenticated:
            await self.close()
            return
        
        # Create or join a consultation room
        if self.user.user_type == 'doctor':
            self.room_group_name = f'doctor_{self.user.id}'
        else:
            # For patients, we'll assign them to available doctors
            self.room_group_name = await self.get_available_doctor_room()
        
        # Join room group
        await self.channel_layer.group_add(
            self.room_group_name,
            self.channel_name
        )
        
        await self.accept()
        
        # Send initial connection message
        await self.send(text_data=json.dumps({
            'type': 'connection_established',
            'message': 'Connected to doctor chat',
            'room': self.room_group_name
        }))
        
        logger.info(f"User {self.user.username} connected to doctor chat: {self.room_group_name}")
    
    async def disconnect(self, close_code):
        # Leave room group
        if hasattr(self, 'room_group_name'):
            await self.channel_layer.group_discard(
                self.room_group_name,
                self.channel_name
            )
        logger.info(f"User disconnected from doctor chat")
    
    async def receive(self, text_data):
        try:
            text_data_json = json.loads(text_data)
            message_type = text_data_json.get('type', 'chat_message')
            
            if message_type == 'chat_message':
                await self.handle_chat_message(text_data_json)
            elif message_type == 'ai_response':
                await self.handle_ai_response(text_data_json)
            elif message_type == 'typing':
                await self.handle_typing(text_data_json)
                
        except Exception as e:
            logger.error(f"Error in doctor chat receive: {e}")
            await self.send(text_data=json.dumps({
                'type': 'error',
                'message': 'An error occurred processing your message'
            }))
    
    async def handle_chat_message(self, data):
        message = data['message']
        
        # Save message to database
        await self.save_consultation_message(message)
        
        # If it's a patient message, generate AI response
        if self.user.user_type == 'patient':
            ai_response = await self.generate_ai_response(message)
            
            # Send patient message to group
            await self.channel_layer.group_send(
                self.room_group_name,
                {
                    'type': 'chat_message',
                    'message': message,
                    'username': self.user.username,
                    'user_type': self.user.user_type,
                    'timestamp': data.get('timestamp')
                }
            )
            
            # Send AI response
            await self.channel_layer.group_send(
                self.room_group_name,
                {
                    'type': 'ai_response',
                    'message': ai_response,
                    'username': 'AI Doctor',
                    'user_type': 'ai_doctor'
                }
            )
        else:
            # Doctor message
            await self.channel_layer.group_send(
                self.room_group_name,
                {
                    'type': 'chat_message',
                    'message': message,
                    'username': self.user.username,
                    'user_type': self.user.user_type,
                    'timestamp': data.get('timestamp')
                }
            )
    
    async def handle_ai_response(self, data):
        # Handle AI-generated responses
        pass
    
    async def handle_typing(self, data):
        # Handle typing indicators
        await self.channel_layer.group_send(
            self.room_group_name,
            {
                'type': 'typing_indicator',
                'username': self.user.username,
                'is_typing': data.get('is_typing', False)
            }
        )
    
    async def chat_message(self, event):
        # Send message to WebSocket
        await self.send(text_data=json.dumps({
            'type': 'chat_message',
            'message': event['message'],
            'username': event['username'],
            'user_type': event.get('user_type', 'patient'),
            'timestamp': event.get('timestamp')
        }))
    
    async def ai_response(self, event):
        # Send AI response to WebSocket
        await self.send(text_data=json.dumps({
            'type': 'ai_response',
            'message': event['message'],
            'username': event['username'],
            'user_type': event.get('user_type', 'ai_doctor')
        }))
    
    async def typing_indicator(self, event):
        # Send typing indicator to WebSocket
        await self.send(text_data=json.dumps({
            'type': 'typing_indicator',
            'username': event['username'],
            'is_typing': event['is_typing']
        }))
    
    @database_sync_to_async
    def get_available_doctor_room(self):
        # Simple logic to assign patient to available doctor
        # In production, this would be more sophisticated
        return 'general_consultation'
    
    @database_sync_to_async
    def save_consultation_message(self, message):
        try:
            from .models import Consultation, ConsultationMessage
            
            # Get or create consultation
            consultation, created = Consultation.objects.get_or_create(
                patient=self.user if self.user.user_type == 'patient' else None,
                defaults={'status': 'active'}
            )
            
            # Save message
            ConsultationMessage.objects.create(
                consultation=consultation,
                sender=self.user,
                content=message
            )
        except Exception as e:
            logger.error(f"Error saving consultation message: {e}")
    
    async def generate_ai_response(self, patient_message):
        """
        Generate AI response to patient message
        This is a simplified version - in production, you'd use a more sophisticated NLP model
        """
        # Simple keyword-based responses
        message_lower = patient_message.lower()
        
        if any(word in message_lower for word in ['fever', 'temperature', 'hot']):
            return "I understand you're experiencing fever. This could indicate an infection or other condition. Please monitor your temperature and consider taking acetaminophen if it's high. If it persists above 101°F (38.3°C) for more than 24 hours, please seek medical attention."
        
        elif any(word in message_lower for word in ['headache', 'head pain']):
            return "Headaches can have various causes including tension, dehydration, or stress. Try resting in a quiet, dark room and staying hydrated. Over-the-counter pain relievers like ibuprofen or acetaminophen may help. If headaches are severe or persistent, please consult a healthcare provider."
        
        elif any(word in message_lower for word in ['cough', 'coughing']):
            return "Coughs can be due to viral infections, allergies, or other respiratory conditions. Stay hydrated and consider honey or throat lozenges for symptom relief. If the cough persists for more than a week, produces blood, or is accompanied by high fever, please seek medical evaluation."
        
        elif any(word in message_lower for word in ['stomach', 'nausea', 'vomit']):
            return "Stomach issues can be caused by various factors including food poisoning, viral infections, or stress. Try staying hydrated with small sips of water or clear fluids. The BRAT diet (bananas, rice, applesauce, toast) may help. If symptoms persist or worsen, please consult a healthcare provider."
        
        elif any(word in message_lower for word in ['pain', 'hurt', 'ache']):
            return "I understand you're experiencing pain. The location and type of pain can help determine the cause. For mild pain, rest and over-the-counter pain relievers may help. However, if the pain is severe, persistent, or accompanied by other concerning symptoms, please seek medical attention promptly."
        
        else:
            return "Thank you for sharing your symptoms with me. Based on what you've described, I recommend monitoring your condition closely. If symptoms persist, worsen, or you develop new concerning symptoms, please don't hesitate to seek medical attention from a healthcare provider. Is there anything specific about your symptoms you'd like to discuss further?"