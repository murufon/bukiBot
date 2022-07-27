from django.contrib import admin
from yaml import serialize
from .models import Server, ServerConfig

# Register your models here.
class ServerAdmin(admin.ModelAdmin):
    readonly_fields = ('created_at', 'updated_at')
    list_display = ('server_name', 'created_at', 'updated_at')

class ServerConfigAdmin(admin.ModelAdmin):
    readonly_fields = ('created_at', 'updated_at')
    list_display = ('server', 'created_at', 'updated_at')

admin.site.register(Server, ServerAdmin)
admin.site.register(ServerConfig, ServerConfigAdmin)