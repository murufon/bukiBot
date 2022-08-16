# coding: UTF-8
import discord
from discord import app_commands

import logging

import os
from os.path import join, dirname
from dotenv import load_dotenv

import json
import random
from typing import Literal

from datetime import date, datetime, timedelta, timezone
import re
import requests

from .models import Server, ServerConfig, RouletteVoiceChat

os.environ["DJANGO_ALLOW_ASYNC_UNSAFE"] = "true"
logging.basicConfig(level=logging.INFO)

# client = discord.Client()
intents = discord.Intents.default()
# intents.message_content = True
client = discord.AutoShardedClient(intents=intents)
tree = app_commands.CommandTree(client)

def getJsonFromAPI(link):
    headers = {"User-Agent": "@murufon"}
    url = "https://spla2.yuu26.com/" + link
    response = requests.get(url,headers=headers)
    json_data = json.loads(response.text)
    return json_data

def getStageInfo(link, key, showRule=True):
    json_data = getJsonFromAPI(link)
    r = json_data['result']
    time_format = '%Y-%m-%dT%H:%M:%S'
    msg = f"{key}のスケジュールはこちら！\n"
    msg += "```\n"
    for i in range(3):
        start = datetime.strptime(r[i]['start'], time_format)
        end = datetime.strptime(r[i]['end'], time_format)
        msg += "\n" # markdownの最初の空行は無視される
        msg += f"{start.strftime('%H:%M')} - {end.strftime('%H:%M')}\n"
        if showRule:
            msg += f"{r[i]['rule']}\n"
        msg += f"{r[i]['maps'][0]}/{r[i]['maps'][1]}\n"
    msg += "```\n"
    return msg

def getCoopInfo(link, key):
    json_data = getJsonFromAPI(link)
    r = json_data['result']
    time_format = '%Y-%m-%dT%H:%M:%S'
    msg = f"{key}のスケジュールはこちら！\n"
    msg += "```\n"
    for i in range(2):
        start = datetime.strptime(r[i]['start'], time_format)
        end = datetime.strptime(r[i]['end'], time_format)
        msg += "\n"
        msg += f"{start.strftime('%m/%d %H:%M')} - {end.strftime('%m/%d %H:%M')}\n"
        msg += f"{r[i]['stage']['name']}\n"
        msg += f"{r[i]['weapons'][0]['name']}/{r[i]['weapons'][1]['name']}/{r[i]['weapons'][2]['name']}/{r[i]['weapons'][3]['name']}\n"
    msg += "```\n"
    return msg

def getDailyRandomString():
    JST = timezone(timedelta(hours=+9), 'JST')
    now = datetime.now(JST)
    now_str = str(now.strftime("%Y%m%d"))
    return now_str

from discord.ext import tasks
if 'GUILD_ID' in os.environ:
    guild = discord.Object(os.environ.get('GUILD_ID'))
else:
    guild = None
@tasks.loop(seconds=60) # TODO: rate limitに引っかかるかも
async def loop():
  await tree.sync(guild=guild)

@client.event
async def on_ready():
    logging.info('-----')
    logging.info('logged in')
    logging.info(f"user name: {client.user.name}")
    logging.info(f"user id: {client.user.id}")
    logging.info(f"discord.py version: {discord.__version__}")
    logging.info("servers connected to:")
    for server in client.guilds:
        logging.info(f"* {server.name}")
    logging.info('-----')
    await tree.sync(guild=guild)
    loop.start()

# @client.event
# async def on_message(message):
#     # メッセージ送信者がBotだった場合は無視する
#     if message.author.bot:
#         return

    # if message.content.lower() in ['buki', 'ぶき', 'ブキ', '武器', 'weapon', 'うえぽん', 'ウエポン']:
    #     json_data = json.load(open('weapon.json','r'))
    #     buki = random.choice(json_data)
    #     ja_name = buki["name"]["ja_JP"]
    #     en_name = buki["name"]["en_US"]
    #     path = "images/main/" + buki["name"]["ja_JP"] + ".png"
    #     user = message.author.display_name
    #     await message.channel.send(f"{user}さんにおすすめのブキは{ja_name}({en_name})！" , file=discord.File(path))

    # if message.content.lower() in ['シューター', 'ブラスター', 'リールガン', 'マニューバー', 'ローラー', 'フデ', 'チャージャー', 'スロッシャー', 'スピナー', 'シェルター']:
    #     type_name = message.content.lower()
    #     json_data = json.load(open('weapon.json','r'))
    #     filtered_data = list(filter(lambda x: x["type"]["name"]["ja_JP"] == type_name, json_data))
    #     if filtered_data:
    #         buki = random.choice(filtered_data)
    #         ja_name = buki["name"]["ja_JP"]
    #         en_name = buki["name"]["en_US"]
    #         path = "images/main/" + buki["name"]["ja_JP"] + ".png"
    #         user = message.author.display_name
    #         await message.channel.send(f"{user}さんにおすすめの{type_name}は{ja_name}({en_name})！" , file=discord.File(path))

    # cmd = message.content.split(" ")
    # if cmd[0] == "/buki" and cmd[1:2]: # cmd[2]が存在するかどうか
    #     type_name = cmd[1]
    #     json_data = json.load(open('weapon.json','r'))
    #     filtered_data = list(filter(lambda x: x["type"]["name"]["ja_JP"] == type_name, json_data))
    #     if filtered_data:
    #         buki = random.choice(filtered_data)
    #         ja_name = buki["name"]["ja_JP"]
    #         en_name = buki["name"]["en_US"]
    #         path = "images/main/" + buki["name"]["ja_JP"] + ".png"
    #         user = message.author.display_name
    #         await message.channel.send(f"{user}さんにおすすめの{type_name}は{ja_name}({en_name})！" , file=discord.File(path))

    # if message.content.lower() in ['gachi', 'ガチ', 'がち', 'gachima', 'ガチマ', 'がちま', 'ガチマッチ', 'がちまっち']:
    #     key = "ガチマッチ"
    #     link = "gachi/schedule"
    #     msg = getStageInfo(link, key)
    #     await message.channel.send(msg)

    # if message.content.lower() in ['league', 'riguma', 'リグマ', 'りぐま', 'リーグマッチ', 'りーぐまっち']:
    #     key = "リーグマッチ"
    #     link = "league/schedule"
    #     msg = getStageInfo(link, key)
    #     await message.channel.send(msg)

    # if message.content.lower() in ['regular', 'レギュラー', 'れぎゅらー', 'レギュラーマッチ', 'れぎゅらーまっち', 'nawabari', 'ナワバリ', 'なわばり', 'ナワバリバトル', 'なわばりばとる']:
    #     key = "ナワバリバトル"
    #     link = "regular/schedule"
    #     msg = getStageInfo(link, key, showRule=False)
    #     await message.channel.send(msg)

    # if message.content.lower() in ['salmon', 'samon', 'sa-mon', 'サーモン', 'さーもん', 'サーモンラン', 'さーもんらん', 'サモラン', 'さもらん', 'coop', 'コープ', 'こーぷ', 'サケ', 'さけ', 'シャケ', 'しゃけ', '鮭']:
    #     key = "サーモンラン"
    #     link = "coop/schedule"
    #     msg = getCoopInfo(link, key)
    #     await message.channel.send(msg)

    # dice_pattern = '^(?P<dice_num>\d+)d(?P<dice_size>\d+)$' # example: 3d6
    # content = message.content.lower()
    # match_result = re.match(dice_pattern, content)
    # if match_result:
    #     dice_num = int(match_result.group('dice_num'))
    #     dice_size = int(match_result.group('dice_size'))
    #     if dice_num < 9999 and dice_size < 9999:
    #         dice_sum = 0
    #         for i in range(dice_num):
    #             dice_sum += random.randint(1, dice_size)
    #         await message.channel.send(str(dice_sum))

    # if 'まそ語録' in message.content:
    #     with open('maso.txt', 'r') as f:
    #         maso_list = f.read().split("\n")
    #     seed = getDailyRandomString() + str(message.author.id)
    #     random.seed(seed)
    #     maso_goroku = random.choice(maso_list)
    #     await message.channel.send(f"今日のまそ語録: {maso_goroku}")

    # if client.user in message.mentions: # if mentioned
    #     if 'おはよ' in message.content:
    #         msg = "おはようございます！"
    #         await message.channel.send(msg)
    #     if 'こんにちは' in message.content:
    #         msg = "こんにちは！"
    #         await message.channel.send(msg)
    #     if 'こんばんは' in message.content:
    #         msg = "こんばんは！"
    #         await message.channel.send(msg)
    #     if 'おやすみ' in message.content:
    #         msg = "おやすみなさい！"
    #         await message.channel.send(msg)
    #     if '好き' in message.content:
    #         msg = "僕も好き！"
    #         await message.channel.send(msg)
    #     if 'たんたん' in message.content:
    #         msg = "初めましてたんたん麺ですよろしくお願いします！"
    #         await message.channel.send(msg)
    #     if 'りつ' in message.content and '晩御飯' in message.content:
    #         with open('ice.txt', 'r') as f:
    #             ice_list = f.read().split("\n")
    #         ice = random.choice(ice_list)
    #         await message.channel.send(f"りつのおすすめ晩御飯: {ice}")

@tree.command(guild=guild, name='buki', description='ブキルーレット')
async def buki(interaction: discord.Interaction):
    json_data = json.load(open('weapon.json','r'))
    buki = random.choice(json_data)
    ja_name = buki["name"]["ja_JP"]
    en_name = buki["name"]["en_US"]
    path = "images/main/" + buki["name"]["ja_JP"] + ".png"
    user = interaction.user.display_name
    await interaction.response.send_message(f"{user}さんにおすすめのブキは{ja_name}({en_name})！", file=discord.File(path))

@tree.command(guild=guild, name='buki_all', description='一括ブキルーレット')
async def buki_all(interaction: discord.Interaction):
    guild = interaction.guild
    if not guild:
        await interaction.response.send_message('サーバーが見つかりません')
    server, created = Server.objects.get_or_create(
        server_id=guild.id,
        defaults={'server_name': guild.name},
    )
    vcs = [v.voicechat_id for v in RouletteVoiceChat.objects.filter(server=server)]
    registered_vcs = [v for v in guild.voice_channels if str(v.id) in vcs]
    if not registered_vcs:
        await interaction.response.send_message('[Error]: チャンネルが登録されていません')
        return
    members = list()
    for vc in registered_vcs:
        members.extend(vc.members)
    if not members:
        await interaction.response.send_message('[Error]: メンバーがいません')
        return
    json_data = json.load(open('weapon.json','r'))
    roulette_results = list()
    for m in members:
        buki = random.choice(json_data)
        ja_name = buki["name"]["ja_JP"]
        en_name = buki["name"]["en_US"]
        # path = "images/main/" + buki["name"]["ja_JP"] + ".png"
        user = m.display_name
        roulette_results.append(f"{user}さんにおすすめのブキは{ja_name}({en_name})！")
    await interaction.response.send_message("\n".join(roulette_results))

def get_registered_channels_msg(server, guild):
    vcs = [v.voicechat_id for v in RouletteVoiceChat.objects.filter(server=server)]
    registered_vcs = [v for v in guild.voice_channels if str(v.id) in vcs]
    if registered_vcs:
        msg = '以下のチャンネルが登録済みです'
        msg += '\n```'
        for v in registered_vcs:
            msg += f'\n* {v.name}'
        msg += '\n```'
    else:
        msg = '登録済みのチャンネルはありません'
    return msg

@tree.command(guild=guild, name='channel_info', description='登録したボイスチャンネル一覧')
async def channel_info(interaction: discord.Interaction):
    guild = interaction.guild
    if not guild:
        await interaction.response.send_message('[Error]: サーバーが見つかりません')
    server, created = Server.objects.get_or_create(
        server_id=guild.id,
        defaults={'server_name': guild.name},
    )
    msg = get_registered_channels_msg(server, guild)
    await interaction.response.send_message(msg)

@tree.command(guild=guild, name='channel_set', description='ボイスチャンネルを登録')
async def channel_set(interaction: discord.Interaction, channel: str):
    guild = interaction.guild
    if not guild:
        await interaction.response.send_message('[Error]: サーバーが見つかりません')
    server, created = Server.objects.get_or_create(
        server_id=guild.id,
        defaults={'server_name': guild.name},
    )

    # voice_channelsのidまたはnameで検索
    voice_channels = [c for c in guild.voice_channels if str(c.id) == channel or str(c.name) == channel]
    if len(voice_channels) > 1:
        msg = f'[Error]: "{channel}"に該当するチャンネルが複数あります'
        msg += '\n' + get_registered_channels_msg(server, guild)
        await interaction.response.send_message(msg)
    elif len(voice_channels) == 1:
        voice_channel = voice_channels[0]
        voicechat = RouletteVoiceChat.objects.filter(server=server, voicechat_id=voice_channel.id)
        if voicechat.exists():
            msg = f'[Error]: "{channel}"はすでに登録されています'
            msg += '\n' + get_registered_channels_msg(server, guild)
            await interaction.response.send_message(msg)
        else:
            vc = RouletteVoiceChat(server=server, voicechat_id=voice_channel.id, voicechat_name=voice_channel.name)
            vc.save()
            msg = f'"{voice_channel.name}"を登録しました'
            msg += '\n' + get_registered_channels_msg(server, guild)
            await interaction.response.send_message(msg)
    else: # len(voice_channels) == 0
        msg = f'[Error]: "{channel}"に該当するチャンネルがありません'
        msg += '\n' + get_registered_channels_msg(server, guild)
        await interaction.response.send_message(msg)

@tree.command(guild=guild, name='channel_remove', description='ボイスチャンネルの登録を解除')
async def channel_remove(interaction: discord.Interaction, channel: str):
    guild = interaction.guild
    if not guild:
        await interaction.response.send_message('[Error]: サーバーが見つかりません')
    server, created = Server.objects.get_or_create(
        server_id=guild.id,
        defaults={'server_name': guild.name},
    )

    # voice_channelsのidまたはnameで検索
    voice_channels = [c for c in guild.voice_channels if str(c.id) == channel or str(c.name) == channel]
    if len(voice_channels) > 1:
        msg = f'[Error]: "{channel}"に該当するチャンネルが複数あります'
        msg += '\n' + get_registered_channels_msg(server, guild)
        await interaction.response.send_message(msg)
    elif len(voice_channels) == 1:
        voice_channel = voice_channels[0]
        voicechat = RouletteVoiceChat.objects.filter(server=server, voicechat_id=voice_channel.id)
        if voicechat.exists():
            vc = voicechat.first()
            vc.delete()
            msg = f'"{voice_channel.name}"を登録解除しました'
            msg += '\n' + get_registered_channels_msg(server, guild)
            await interaction.response.send_message(msg)
        else:
            msg = f'[Error]: "{channel}"に該当するチャンネルは登録されていません'
            msg += '\n' + get_registered_channels_msg(server, guild)
            await interaction.response.send_message(msg)
    else: # len(voice_channels) == 0
        msg = f'[Error]: "{channel}"に該当するチャンネルがありません'
        msg += '\n' + get_registered_channels_msg(server, guild)
        await interaction.response.send_message(msg)

@tree.command(guild=guild, name='buki_type', description='ブキ種ごとのルーレット')
@app_commands.describe(type='ブキの種類')
async def buki_type(interaction: discord.Interaction, type: Literal['シューター', 'ブラスター', 'リールガン', 'マニューバー', 'ローラー', 'フデ', 'チャージャー', 'スロッシャー', 'スピナー', 'シェルター']):
    json_data = json.load(open('weapon.json','r'))
    filtered_data = list(filter(lambda x: x["type"]["name"]["ja_JP"] == type, json_data))
    if filtered_data:
        buki = random.choice(filtered_data)
        ja_name = buki["name"]["ja_JP"]
        en_name = buki["name"]["en_US"]
        path = "images/main/" + buki["name"]["ja_JP"] + ".png"
        user = interaction.user.display_name
        await interaction.response.send_message(f"{user}さんにおすすめの{type}は{ja_name}({en_name})！" , file=discord.File(path))

@tree.command(guild=guild, name='gachima', description='ガチマッチのスケジュールを表示')
async def gachima(interaction: discord.Interaction):
    key = "ガチマッチ"
    link = "gachi/schedule"
    msg = getStageInfo(link, key)
    await interaction.response.send_message(msg)

@tree.command(guild=guild)
async def riguma(interaction: discord.Interaction):
    key = "リーグマッチ"
    link = "league/schedule"
    msg = getStageInfo(link, key)
    await interaction.response.send_message(msg)

@tree.command(guild=guild, name='nawabari', description='ナワバリバトルのスケジュールを表示')
async def nawabari(interaction: discord.Interaction):
    key = "ナワバリバトル"
    link = "regular/schedule"
    msg = getStageInfo(link, key, showRule=False)
    await interaction.response.send_message(msg)

@tree.command(guild=guild, name='salmon', description='サーモンランのスケジュールを表示')
async def salmon(interaction: discord.Interaction):
    key = "サーモンラン"
    link = "coop/schedule"
    msg = getCoopInfo(link, key)
    await interaction.response.send_message(msg)

@tree.command(guild=guild, name='countdown', description='Splatoon3までの残り日数を表示')
async def countdown(interaction: discord.Interaction):
    JST = timezone(timedelta(hours=+9), 'JST')
    end_day = datetime(2022, 9, 9, tzinfo=JST)
    today = datetime.now(JST)
    delta = end_day - today
    days = delta.days + 1
    logging.info(end_day)
    logging.info(today)
    logging.info(delta)
    if days > 0:
        msg = "Splatoon3発売まであと" + str(days) + "日！！"
    else:
        msg = "Splatoon3発売！！"
    await interaction.response.send_message(msg)

# @tree.command(guild=guild)
# async def dice(interaction: discord.Interaction):
#     pass

def run(DISCORDBOT_TOKEN):
    client.run(DISCORDBOT_TOKEN)

if __name__ == '__main__':
    logging.info("[Bot] - You must run this bot via your manage.py file: python manage.py run-discorbot")
