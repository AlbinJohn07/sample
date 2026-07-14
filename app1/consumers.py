"""
WebSocket consumers for real-time notifications
Handles WebSocket connections and real-time notification broadcasting
"""

import json
from channels.generic.websocket import AsyncWebsocketConsumer
from channels.db import database_sync_to_async
from django.contrib.auth import get_user_model
from .models import Notification

User = get_user_model()


class NotificationConsumer(AsyncWebsocketConsumer):
    """
    WebSocket consumer for real-time notifications
    Handles user-specific notification channels
    """
    
    async def connect(self):
        """Handle WebSocket connection"""
        self.user = self.scope["user"]
        
        # Only allow authenticated users
        if self.user.is_anonymous:
            await self.close()
            return
        
        # Create user-specific group name
        self.group_name = f"notifications_{self.user.id}"
        
        # Join user-specific notification group
        await self.channel_layer.group_add(
            self.group_name,
            self.channel_name
        )
        
        await self.accept()
        
        # Send initial notification count
        unread_count = await self.get_unread_count()
        await self.send(text_data=json.dumps({
            'type': 'notification_count',
            'unread_count': unread_count
        }))
    
    async def disconnect(self, close_code):
        """Handle WebSocket disconnection"""
        if hasattr(self, 'group_name'):
            await self.channel_layer.group_discard(
                self.group_name,
                self.channel_name
            )
    
    async def receive(self, text_data):
        """Handle messages from WebSocket"""
        try:
            text_data_json = json.loads(text_data)
            message_type = text_data_json.get('type')
            
            if message_type == 'mark_read':
                notification_id = text_data_json.get('notification_id')
                if notification_id:
                    await self.mark_notification_read(notification_id)
            
            elif message_type == 'mark_all_read':
                await self.mark_all_notifications_read()
            
            elif message_type == 'get_notifications':
                notifications = await self.get_recent_notifications()
                await self.send(text_data=json.dumps({
                    'type': 'notifications_list',
                    'notifications': notifications
                }))
                
        except json.JSONDecodeError:
            await self.send(text_data=json.dumps({
                'type': 'error',
                'message': 'Invalid JSON format'
            }))
    
    async def notification_message(self, event):
        """Handle notification broadcast to user"""
        await self.send(text_data=json.dumps({
            'type': 'new_notification',
            'notification': event['notification']
        }))
    
    async def notification_count_update(self, event):
        """Handle notification count updates"""
        await self.send(text_data=json.dumps({
            'type': 'notification_count',
            'unread_count': event['unread_count']
        }))
    
    @database_sync_to_async
    def get_unread_count(self):
        """Get unread notification count for user"""
        return Notification.objects.filter(
            recipient=self.user,
            is_read=False
        ).count()
    
    @database_sync_to_async
    def mark_notification_read(self, notification_id):
        """Mark a specific notification as read"""
        try:
            notification = Notification.objects.get(
                id=notification_id,
                recipient=self.user
            )
            notification.mark_as_read()
            return True
        except Notification.DoesNotExist:
            return False
    
    @database_sync_to_async
    def mark_all_notifications_read(self):
        """Mark all notifications as read for user"""
        notifications = Notification.objects.filter(
            recipient=self.user,
            is_read=False
        )
        for notification in notifications:
            notification.mark_as_read()
        return notifications.count()
    
    @database_sync_to_async
    def get_recent_notifications(self):
        """Get recent notifications for user"""
        from .serializers import NotificationSerializer
        
        notifications = Notification.objects.filter(
            recipient=self.user
        ).order_by('-created_at')[:20]
        
        serializer = NotificationSerializer(notifications, many=True)
        return serializer.data


class SystemNotificationConsumer(AsyncWebsocketConsumer):
    """
    WebSocket consumer for system-wide notifications
    Handles admin/management notifications
    """
    
    async def connect(self):
        """Handle WebSocket connection"""
        self.user = self.scope["user"]
        
        # Only allow admin/management users
        if self.user.is_anonymous or self.user.role not in ['admin', 'management']:
            await self.close()
            return
        
        # Join system notification group
        self.group_name = "system_notifications"
        
        await self.channel_layer.group_add(
            self.group_name,
            self.channel_name
        )
        
        await self.accept()
    
    async def disconnect(self, close_code):
        """Handle WebSocket disconnection"""
        if hasattr(self, 'group_name'):
            await self.channel_layer.group_discard(
                self.group_name,
                self.channel_name
            )
    
    async def system_notification(self, event):
        """Handle system notification broadcast"""
        await self.send(text_data=json.dumps({
            'type': 'system_notification',
            'notification': event['notification']
        }))


# Utility functions for broadcasting notifications
from channels.layers import get_channel_layer
from asgiref.sync import async_to_sync

def broadcast_notification_to_user(user_id, notification_data):
    """
    Broadcast notification to a specific user
    """
    channel_layer = get_channel_layer()
    group_name = f"notifications_{user_id}"
    
    async_to_sync(channel_layer.group_send)(
        group_name,
        {
            'type': 'notification_message',
            'notification': notification_data
        }
    )

def broadcast_notification_count_to_user(user_id, unread_count):
    """
    Broadcast notification count update to a specific user
    """
    channel_layer = get_channel_layer()
    group_name = f"notifications_{user_id}"
    
    async_to_sync(channel_layer.group_send)(
        group_name,
        {
            'type': 'notification_count_update',
            'unread_count': unread_count
        }
    )

def broadcast_system_notification(notification_data):
    """
    Broadcast system notification to all admin users
    """
    channel_layer = get_channel_layer()
    
    async_to_sync(channel_layer.group_send)(
        "system_notifications",
        {
            'type': 'system_notification',
            'notification': notification_data
        }
    )
