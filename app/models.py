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
    server = models.OneToOneField(Server, verbose_name='サーバー', related_name='config', on_delete=models.CASCADE)
    splatoon2_textchat_id = models.CharField('Splatoon2用テキストチャットID', max_length=50) # DiscordのチャンネルIDは18文字
    splatoon3_textchat_id = models.CharField('Splatoon3用テキストチャットID', max_length=50) # DiscordのチャンネルIDは18文字
    created_at = models.DateTimeField('作成日', auto_now_add=True)
    updated_at = models.DateTimeField('更新日', auto_now=True)
    def __str__(self):
        return self.server.server_name

class RouletteVoiceChat(models.Model):
    server = models.ForeignKey(Server, verbose_name='サーバー', related_name='roulette_voicechat', on_delete=models.CASCADE)
    voicechat_id = models.CharField('ボイスチャットID', help_text='ルーレットを有効化するボイスチャットのID', max_length=50) # DiscordのチャンネルIDは18文字
    voicechat_name = models.CharField('ボイスチャット名', max_length=200) # 登録時のname. Discordのチャンネル名は100文字まで