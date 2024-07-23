from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import TaskNotification, EventNotification, AdminNotification
from channels.layers import get_channel_layer
from asgiref.sync import async_to_sync
import json

@receiver(post_save, sender=TaskNotification)
def task_notification_handler(sender, instance, created, **kwargs):
    if created:
        channel_layer = get_channel_layer()
        async_to_sync(channel_layer.group_send)(
            'notifications',
            {
                'type': 'send_notification',
                'notification': {
                    'type': 'task',
                    'task_id': str(instance.task_id),
                    'title': instance.title,
                    'icon': instance.icon,
                    'start_date': str(instance.start_date),
                    'end_date': str(instance.end_date),
                }
            }
        )

@receiver(post_save, sender=EventNotification)
def event_notification_handler(sender, instance, created, **kwargs):
    if created:
        channel_layer = get_channel_layer()
        async_to_sync(channel_layer.group_send)(
            'notifications',
            {
                'type': 'send_notification',
                'notification': {
                    'type': 'event',
                    'event_id': str(instance.event_id),
                    'title': instance.title,
                    'icon': instance.icon,
                    'start_date': str(instance.start_date),
                    'end_date': str(instance.end_date),
                }
            }
        )

@receiver(post_save, sender=AdminNotification)
def admin_notification_handler(sender, instance, created, **kwargs):
    if created:
        channel_layer = get_channel_layer()
        async_to_sync(channel_layer.group_send)(
            'notifications',
            {
                'type': 'send_notification',
                'notification': {
                    'type': 'admin',
                    'notification_id': str(instance.notification_id),
                    'title': instance.title,
                    'icon': instance.icon,
                    'content': instance.content,
                    'additional_data': instance.additional_data,
                    'date': str(instance.date),
                }
            }
        )
