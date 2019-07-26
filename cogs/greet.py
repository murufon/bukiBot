from discord.ext import commands # Bot Commands Frameworkのインポート

# コグとして用いるクラスを定義
class GreetCog(commands.Cog):

    # TestCogクラスのコンストラクタ。Botを受取り、インスタンス変数として保持
    def __init__(self, bot):
        self.bot = bot

    # コマンドの作成。コマンドはcommandデコレータで必ず修飾する
    @commands.command()
    async def ping(self, ctx):
        await ctx.send('pong!')

    @commands.command()
    async def neko(self, ctx):
        await ctx.send('にゃーん!!!')

    # @commands.Cog.listener()
    # async def on_member_join(member):
    #     print(member)
    #     channel = client.get_channel('562638392672780288')
    #     name = member.display_name
    #     print(name)
    #     await client.send_message(channel, name)

    # @commands.command()
    # async def what(self, ctx, what):
    #     await ctx.send(f'{what}とはなんですか？')

# Bot本体側からコグを読み込む際に呼び出される関数
def setup(bot):
    bot.add_cog(GreetCog(bot)) # TestCogにBotを渡してインスタンス化し、Botにコグとして登録する
