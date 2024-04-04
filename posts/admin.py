from django.contrib import admin
from posts.models import Message, Thread

class MessageAdmin(admin.ModelAdmin):
    list_display = ['pk', 'sender', 'text', 'thread', 'created_at', 'is_read']
    list_filter = ['sender', 'thread', 'created_at', 'is_read']
    search_fields = ['sender', 'text', 'thread', 'created_at', 'is_read']

class ThreadAdmin(admin.ModelAdmin):
    list_display = ['pk', 'created_at', 'updated_at']
    list_filter = ['participants', 'created_at', 'updated_at']
    search_fields = ['participants', 'created_at', 'updated_at']

admin.site.register(Message, MessageAdmin)
admin.site.register(Thread, ThreadAdmin)

