import datetime
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
    start_date = models.DateTimeField(default=datetime.datetime.now)
    due_date = models.DateTimeField(default=timezone.now()+timezone.timedelta(days=1))
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
    startDate = models.DateField(default=datetime.date.today)
    endDate = models.DateField(default=datetime.date.today)
    startTime = models.TimeField(default=datetime.time())
    endTime = models.TimeField(default=datetime.time())
    is_all_day = models.BooleanField(default=False)
    created_at = models.DateField(auto_now_add=True)
    updated_at = models.DateField(auto_now=True)

