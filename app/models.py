from http import server
from django.db import models

# Create your models here.
class Server(models.Model):
    server_id = models.CharField('サーバーID', max_length=50) # DiscordのサーバーIDは18文字
    server_name = models.CharField('サーバー名', max_length=200) # Discordのサーバー名は100文字まで
    created_at = models.DateTimeField('作成日', auto_now_add=True)
    updated_at = models.DateTimeField('更新日', auto_now=True)
    def __str__(self):
        return self.server_name

class ServerConfig(models.Model):
    server = models.OneToOneField(Server, verbose_name='サーバー設定', related_name='config', on_delete=models.CASCADE)
    splatoon2_textchat_id = models.CharField('Splatoon2用テキストチャット', max_length=50) # DiscordのチャンネルIDは18文字
    splatoon3_textchat_id = models.CharField('Splatoon3用テキストチャット', max_length=50) # DiscordのチャンネルIDは18文字
    created_at = models.DateTimeField('作成日', auto_now_add=True)
    updated_at = models.DateTimeField('更新日', auto_now=True)
    def __str__(self):
        return self.server.server_name
