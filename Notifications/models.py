from django.db import models
import uuid
from django.utils import timezone

class Notification(models.Model):
    type = models.CharField(max_length=50)
    title = models.CharField(max_length=200)
    icon = models.CharField(max_length=200)
    date = models.DateTimeField(default=timezone.now)

    class Meta:
        abstract = True

    def __str__(self):
        return self.title

class TaskNotification(Notification):
    task_id = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)
    start_date = models.DateTimeField()
    end_date = models.DateTimeField()

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['task_id'], name='unique_task_id')
        ]

class EventNotification(Notification):
    event_id = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)
    start_date = models.DateTimeField()
    end_date = models.DateTimeField()

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['event_id'], name='unique_event_id')
        ]

class AdminNotification(Notification):
    notification_id = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)
    content = models.TextField()
    additional_data = models.JSONField(default=dict)

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['notification_id'], name='unique_notification_id')
        ]
