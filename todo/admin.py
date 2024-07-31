from django.contrib import admin
from todo.models import *
@admin.register(Task)
class VersionsAdmin(admin.ModelAdmin):
    pass


@admin.register(Event)
class VersionsAdmin(admin.ModelAdmin):
    pass

@admin.register(Expense)
class VersionsAdmin(admin.ModelAdmin):
    pass

@admin.register(Icon)
class VersionsAdmin(admin.ModelAdmin):
    pass