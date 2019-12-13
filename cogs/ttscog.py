import discord
from discord.ext import commands
import os
from google.cloud import texttospeech
import datetime
import re
import asyncio

class TTSCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_message(self, ctx):
        # botは読み上げない
        if ctx.author.bot:
            return

        mess_id = ctx.author.id
        guild_id = ctx.guild.id # サーバID
        prefix = "!"

        if ctx.content.startswith(prefix):
            return

        # そのギルドでVC接続されているか判別
        if ctx.guild.voice_client is not None:
            if ctx.guild.voice_client.is_connected():
                ctrlvc = ctx.guild.voice_client
            else:
                return
        else:
            return

        str_guild_id = str(guild_id)

        get_msg = ctx.clean_content
        # URLを、"URL"へ置換
        get_msg = re.sub(r'http(s)?://([\w-]+\.)+[\w-]+(/[-\w ./?%&=]*)?', 'URL', get_msg)
        # reactionの置換
        get_msg = re.sub(':(\w\w+):\d+', r'\1', get_msg)
        # 「<>」の削除
        get_msg = re.sub('[<>]', '', get_msg)
        # 「&」の置換
        get_msg = get_msg.replace('&', '&amp;')

        rawfile = self.knockGTTS(get_msg, str_guild_id)
        voice_mess = './tmp/{}/{}'.format(str_guild_id, rawfile)
        query = voice_mess

        source = discord.PCMVolumeTransformer(discord.FFmpegPCMAudio(query))
        ctrlvc = ctx.guild.voice_client
        # ctx.voice_client.play(source, after=lambda e: print('Player error: %s' % e) if e else None)
        while (ctrlvc.is_playing()):
            # 他の処理をさせて1秒待機
            await asyncio.sleep(1)



        ctrlvc.play(discord.FFmpegPCMAudio(query))

        # try:
        #     await ctx.channel.send(file=yurushite)
        #     yurushite_f.close()
        # except NameError:
        #     pass

        # await ctx.channel.send('Now playing: {}'.format(query))
        # await asyncio.sleep(0.5)
        # os.remove(query)

        print("on_message" + ctx.clean_content)

    @commands.command()
    async def join(self, ctx, *, channel: discord.VoiceChannel):
        """Joins a voice channel"""

        if ctx.voice_client is not None:
            return await ctx.voice_client.move_to(channel)

        await channel.connect()

    @commands.command()
    async def play(self, ctx, *, query):
        # """Plays a file from the local filesystem"""

        guild_id = ctx.guild.id
        str_guild_id = str(guild_id)
        # get_msg = ctx.clean_content
        get_msg = query
        # URLを、"URL"へ置換
        get_msg = re.sub(r'http(s)?://([\w-]+\.)+[\w-]+(/[-\w ./?%&=]*)?', 'URL', get_msg)
        # reactionの置換
        get_msg = re.sub(':(\w\w+):\d+', r'\1', get_msg)
        # 「<>」の削除
        get_msg = re.sub('[<>]', '', get_msg)
        # 「&」の置換
        get_msg = get_msg.replace('&', '&amp;')

        print(get_msg)

        rawfile = self.knockGTTS(get_msg, str_guild_id)
        voice_mess = './tmp/{}/{}'.format(str_guild_id, rawfile)
        query = voice_mess

        source = discord.PCMVolumeTransformer(discord.FFmpegPCMAudio(query))
        ctx.voice_client.play(source, after=lambda e: print('Player error: %s' % e) if e else None)

        await ctx.send('Now playing: {}'.format(query))
        os.remove(voice_mess)

    @commands.command()
    async def volume(self, ctx, volume: int):
        """Changes the player's volume"""

        if ctx.voice_client is None:
            return await ctx.send("Not connected to a voice channel.")

        ctx.voice_client.source.volume = volume / 100
        await ctx.send("Changed volume to {}%".format(volume))

    @commands.command()
    async def stop(self, ctx):
        """Stops and disconnects the bot from voice"""

        await ctx.voice_client.disconnect()

    @play.before_invoke
    async def ensure_voice(self, ctx):
        if ctx.voice_client is None:
            if ctx.author.voice:
                await ctx.author.voice.channel.connect()
            else:
                await ctx.send("You are not connected to a voice channel.")
                raise commands.CommandError("Author not connected to a voice channel.")
        elif ctx.voice_client.is_playing():
            ctx.voice_client.stop()

    gtclient = texttospeech.TextToSpeechClient()
    def knockGTTS(self, makemsg, group):
        #バイナリデータの一時保存場所
        tmp = "./tmp/{}/".format(group)

        if not os.path.isdir(tmp):
            os.makedirs(tmp)

        input_text = texttospeech.types.SynthesisInput(text=makemsg)

        voice = texttospeech.types.VoiceSelectionParams(
            language_code='ja-JP',
            # language_code='en-US',
            ssml_gender=texttospeech.enums.SsmlVoiceGender.FEMALE)

        audio_config = texttospeech.types.AudioConfig(
            audio_encoding=texttospeech.enums.AudioEncoding.MP3)

        response = self.gtclient.synthesize_speech(input_text, voice, audio_config)

        #現在日時を取得
        now = datetime.datetime.now()
        tstr = datetime.datetime.strftime(now, '%Y%m%d-%H%M%S%f')

        #保存するファイル名
        rawFile = tstr + ".raw"

        #バイナリデータを保存
        fp = open(tmp + rawFile, 'wb')
        fp.write(response.audio_content)
        fp.close()
        
        # PCM名を返す
        return rawFile

def setup(bot):
    bot.add_cog(TTSCog(bot))
