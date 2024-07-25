from rest_framework import serializers

from django.contrib.auth import get_user_model
from rest_framework.serializers import ModelSerializer

from .models import CustomUser
from todo.models import *
User = get_user_model()



class TaskCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Task
        fields = ('title','icon','priority','icon_color','notes',
                  'start_date','due_date','completed','geoPoint')

class TaskUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Task
        fields = ('title','icon','priority','icon_color',
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
        fields = '__all__'

class EventUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Event
        fields = '__all__'
class EventListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Event
        fields = '__all__'
