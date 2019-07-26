# coding: UTF-8
import discord
from discord.ext import commands
import traceback

import os
from os.path import join, dirname
from dotenv import load_dotenv

# Botトークンの読み込み
BOT_TOKEN_KEY = "BOT_TOKEN"
if BOT_TOKEN_KEY not in os.environ:
    dotenv_path = join(dirname(__file__), '.env')
    load_dotenv(dotenv_path)
BOT_TOKEN = os.environ.get(BOT_TOKEN_KEY)

# 読み込むコグのリスト
INITIAL_COGS = [
    'cogs.buki'
]

class MyBot(commands.Bot):

    # MyBotのコンストラクタ
    def __init__(self, command_prefix):
        # スーパークラスのコンストラクタに値を渡して実行
        super().__init__(command_prefix)

        # INITIAL_COGSに格納されている名前から、コグを読み込む
        # エラーが発生した場合は、エラー内容を表示
        for cog in INITIAL_COGS:
            try:
                self.load_extension(cog)
            except Exception:
                traceback.print_exc()

    # Botの準備完了時に呼び出されるイベント
    async def on_ready(self):
        print('-----')
        print('logged in')
        print('user name: ' + str(self.user.name))
        print('user id: ' + str(self.user.id))
        print('-----')

    # メッセージを受信した際に呼び出されるイベント
    async def on_message(self, message):
        if message.author.bot: # メッセージの送信者がBotなら、処理を終了する
            return

        await self.process_commands(message) # messageがコマンドなら実行する処理

# MyBotのインスタンス化及び起動処理
if __name__ == '__main__':
    bot = MyBot(command_prefix='') # command_prefixはコマンドの最初の文字として使うもの。 e.g. !ping
    bot.run(BOT_TOKEN) # Botのトークン
