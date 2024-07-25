import uuid
from django.db import models
from django.db.models import UniqueConstraint
from django.utils import timezone
from account.models import CustomUser
import json

class Task(models.Model):
    uuid = models.UUIDField(primary_key=True,default=uuid.uuid4, editable=False)
    title = models.CharField(max_length=255)
    icon = models.CharField(max_length=255)
    priority = models.CharField(max_length=255,default=0)
    icon_color = models.CharField(max_length=255)
    notes = models.CharField(max_length=255)
    start_date = models.DateTimeField(auto_now_add=True)
    due_date = models.DateTimeField(auto_now=True)
    completed = models.BooleanField(default=False)
    geoPoint = models.CharField(max_length=255)
    created_at = models.DateField(auto_now_add=True)
    updated_at = models.DateField(auto_now=True)




class Expense(models.Model):
    uuid = models.UUIDField(primary_key=True,default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=255)
    title = models.CharField(max_length=255)
    description = models.CharField(max_length=255)
    icon = models.CharField(max_length=255)
    price = models.DecimalField(max_digits=5, decimal_places=2, default=0)
    is_income = models.BooleanField(default=False)

class Event(models.Model):
    uuid = models.UUIDField(primary_key=True,default=uuid.uuid4, editable=False)
    event_name = models.CharField(max_length=255)
    repeatTime = models.CharField(max_length=255)
    selectIconIndex = models.IntegerField(default=0)
    addNote = models.CharField(max_length=255,null=True)
    startDate = models.DateField(auto_now_add=True)
    endDate = models.DateField(auto_now=True)
    startTime = models.TimeField(auto_now_add=True)
    endTime = models.TimeField(auto_now=True)
    is_all_day = models.BooleanField(default=False)
    created_at = models.DateField(auto_now_add=True)
    updated_at = models.DateField(auto_now=True)

