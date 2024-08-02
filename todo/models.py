import datetime
import uuid
from django.db import models
from django.utils import timezone
from account.models import CustomUser

class Task(models.Model):
    uuid = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    title = models.CharField(max_length=255)
    icon = models.ForeignKey('Icon', related_name='task_icons', on_delete=models.CASCADE)
    iconColor = models.ForeignKey('IconColor', related_name='task_icons_color', on_delete=models.CASCADE, default=1)
    priority = models.CharField(max_length=255, default='0')
    notes = models.CharField(max_length=255, null=True, blank=True)
    start_date = models.DateTimeField(default=timezone.now)
    due_date = models.DateTimeField(default= timezone.now() + timezone.timedelta(days=1), null=True)
    completed = models.BooleanField(default=False)
    geoPoint = models.CharField(max_length=255, null=True, blank=True)
    created_at = models.DateField(auto_now_add=True, null=True)
    updated_at = models.DateField(auto_now=True,null=True)

class Expense(models.Model):
    uuid = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=255)
    title = models.CharField(max_length=255)
    description = models.CharField(max_length=255)
    icon = models.ForeignKey("Icon", related_name='expense_icons', on_delete=models.CASCADE)
    iconColor = models.ForeignKey('IconColor', related_name='expense_icons_color', on_delete=models.CASCADE, default=1)
    price = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    is_income = models.BooleanField(default=False)
    created_at = models.DateField(auto_now_add=True,null=True)
    updated_at = models.DateField(auto_now=True,null=True)

class Event(models.Model):
    uuid = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    event_name = models.CharField(max_length=255)
    repeatTime = models.CharField(max_length=255)
    icon = models.ForeignKey("Icon", related_name='event_icons', on_delete=models.CASCADE, null=True)
    iconColor = models.ForeignKey('IconColor', related_name='event_icons_color', on_delete=models.CASCADE, null=True)
    addNote = models.CharField(max_length=255, null=True, blank=True)
    startDate = models.DateField(default=timezone.now)
    endDate = models.DateField(default= timezone.now() + timezone.timedelta(days=1))
    startTime = models.TimeField(default=timezone.now)
    endTime = models.TimeField(default=timezone.now)
    is_all_day = models.BooleanField(default=False)
    created_at = models.DateField(auto_now_add=True,null=True)
    updated_at = models.DateField(auto_now=True,null=True)

class Icon(models.Model):
    uuid = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=255)
    image = models.FileField(upload_to='icons/')
    created_at = models.DateField(auto_now_add=True,null=True)
    updated_at = models.DateField(auto_now=True,null=True)
    def __str__(self):
        return self.name
class IconColor(models.Model):
    color = models.CharField(max_length=255)
    created_at = models.DateField(auto_now_add=True,null=True)
    updated_at = models.DateField(auto_now=True,null=True)

    def __str__(self):
        return self.color
