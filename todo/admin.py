from django.contrib import admin
from todo.models import *
@admin.register(Task)
class VersionsAdmin(admin.ModelAdmin):
    list_display = ( 'title', 'priority', 'completed' )


@admin.register(Event)
class VersionsAdmin(admin.ModelAdmin):
    list_display = ('event_name',"startDate")
    search_fields = ('event_name',)

@admin.register(Expense)
class VersionsAdmin(admin.ModelAdmin):
    list_display = ('name',"title",'price')
    search_fields = ('name','title','price')
@admin.register(IconColor)
class VersionsAdmin(admin.ModelAdmin):
    pass

class IconAdmin(admin.ModelAdmin):
    list_display = ('name', 'uuid', 'created_at', 'updated_at')
    search_fields = ('name',)

admin.site.register(Icon, IconAdmin)