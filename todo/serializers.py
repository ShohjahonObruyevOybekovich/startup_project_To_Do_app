from rest_framework import serializers

from django.contrib.auth import get_user_model
from rest_framework.serializers import ModelSerializer

from .models import CustomUser
from todo.models import *
User = get_user_model()


class TaskCreateSerializer(serializers.ModelSerializer):
    # icon = serializers.SerializerMethodField()
    class Meta:
        model = Task
        fields = ('title','icon','priority','notes',
                  'start_date','due_date','completed','geoPoint')

class TaskUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Task
        fields = ('title','icon','priority',
                  'notes','start_date','due_date','completed','geoPoint')

class TaskListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Task
        fields = '__all__'

class ExpenseCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Expense
        fields = '__all__'

class ExpenseUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Expense
        fields = '__all__'
class ExpenseListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Expense
        fields = '__all__'

class EventCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Event
        fields = ('uuid','event_name','repeatTime','icon','addNote'
                  ,'startDate','endDate','startTime','endTime','is_all_day','created_at')

class EventUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Event
        fields = '__all__'
class EventListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Event
        fields = '__all__'

class IconListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Icon
        fields = '__all__'

