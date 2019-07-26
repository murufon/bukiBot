# Bot Commands Frameworkのインポート
from discord.ext import commands

import json
import random

# コグとして用いるクラスを定義
class BukiCog(commands.Cog):
    json_data = json.load(open('weapon.json','r'))
    print("json data loaded")

    # クラスのコンストラクタ。Botを受取り、インスタンス変数として保持
    def __init__(self, bot):
        self.bot = bot

    # コマンドの作成。コマンドはcommandデコレータで必ず修飾する
    @commands.command(aliases=["ぶき","ブキ","武器"],prefix="!")
    async def buki(self, ctx):
        buki = random.choice(self.json_data)
        await ctx.send(buki["name"]["ja_JP"])
        # print("{}".format(json.dumps(self.json_data,indent=4)))

    # @commands.command(name="ブキ", )
    # async def buki1(self, ctx):
    #     buki = random.choice(self.json_data)
    #     await ctx.send(buki["name"]["ja_JP"])
    #     # print("{}".format(json.dumps(self.json_data,indent=4)))

# Bot本体側からコグを読み込む際に呼び出される関数
def setup(bot):
    bot.add_cog(BukiCog(bot)) # Botを渡してインスタンス化し、Botにコグとして登録する
