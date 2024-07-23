from django.contrib import admin
from .models import TaskNotification, EventNotification, AdminNotification

@admin.register(TaskNotification)
class TaskNotificationAdmin(admin.ModelAdmin):
    list_display = ('title', 'start_date', 'end_date')

@admin.register(EventNotification)
class EventNotificationAdmin(admin.ModelAdmin):
    list_display = ('title', 'start_date', 'end_date')

@admin.register(AdminNotification)
class AdminNotificationAdmin(admin.ModelAdmin):
    list_display = ('title', 'date', 'notification_id')
