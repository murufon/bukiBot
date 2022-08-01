from django.contrib import admin
from yaml import serialize
from .models import Server, ServerConfig, RouletteVoiceChat

# Register your models here.
class ServerAdmin(admin.ModelAdmin):
    readonly_fields = ('created_at', 'updated_at')
    list_display = ('server_name', 'created_at', 'updated_at')

class ServerConfigAdmin(admin.ModelAdmin):
    readonly_fields = ('created_at', 'updated_at')
    list_display = ('server', 'created_at', 'updated_at')

class RouletteVoiceChatAdmin(admin.ModelAdmin):
    list_display = ('server', 'voicechat_name', 'voicechat_id')


admin.site.register(Server, ServerAdmin)
admin.site.register(ServerConfig, ServerConfigAdmin)
admin.site.register(RouletteVoiceChat, RouletteVoiceChatAdmin)