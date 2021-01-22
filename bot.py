# coding: UTF-8
import discord
import logging

import os
from os.path import join, dirname
from dotenv import load_dotenv

import json
import random

import datetime
import re
import requests

logging.basicConfig(level=logging.INFO)

client = discord.Client()

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
        start = datetime.datetime.strptime(r[i]['start'], time_format)
        end = datetime.datetime.strptime(r[i]['end'], time_format)
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
        start = datetime.datetime.strptime(r[i]['start'], time_format)
        end = datetime.datetime.strptime(r[i]['end'], time_format)
        msg += "\n"
        msg += f"{start.strftime('%m/%d %H:%M')} - {end.strftime('%m/%d %H:%M')}\n"
        msg += f"{r[i]['stage']['name']}\n"
        msg += f"{r[i]['weapons'][0]['name']}/{r[i]['weapons'][1]['name']}/{r[i]['weapons'][2]['name']}/{r[i]['weapons'][3]['name']}\n"
    msg += "```\n"
    return msg

def getDailyRandomString():
    now = datetime.datetime.now()
    now_str = str(now.strftime("%Y%m%d"))
    return now_str

@client.event
async def on_ready():
    print('-----')
    print('logged in')
    print(f"user name: {client.user.name}")
    print(f"user id: {client.user.id}")
    print(f"discord.py version: {discord.__version__}")
    print("servers connected to:")
    for server in client.guilds:
        print(f"* {server.name}")
    print('-----')

@client.event
async def on_message(message):
    # メッセージ送信者がBotだった場合は無視する
    if message.author.bot:
        return

    if message.content.lower() in ['buki', 'ぶき', 'ブキ', '武器', 'weapon', 'うえぽん', 'ウエポン']:
        json_data = json.load(open('weapon.json','r'))
        buki = random.choice(json_data)
        ja_name = buki["name"]["ja_JP"]
        en_name = buki["name"]["en_US"]
        path = "images/main/" + buki["name"]["ja_JP"] + ".png"
        user = message.author.display_name
        await message.channel.send(f"{user}さんにおすすめのブキは{ja_name}({en_name})！" , file=discord.File(path))

    if message.content.lower() in ['シューター', 'ブラスター', 'リールガン', 'マニューバー', 'ローラー', 'フデ', 'チャージャー', 'スロッシャー', 'スピナー', 'シェルター']:
        type_name = message.content.lower()
        json_data = json.load(open('weapon.json','r'))
        filtered_data = list(filter(lambda x: x["type"]["name"]["ja_JP"] == type_name, json_data))
        if filtered_data:
            buki = random.choice(filtered_data)
            ja_name = buki["name"]["ja_JP"]
            en_name = buki["name"]["en_US"]
            path = "images/main/" + buki["name"]["ja_JP"] + ".png"
            user = message.author.display_name
            await message.channel.send(f"{user}さんにおすすめの{type_name}は{ja_name}({en_name})！" , file=discord.File(path))

    cmd = message.content.split(" ")
    if cmd[0] == "/buki" and cmd[1:2]: # cmd[2]が存在するかどうか
        type_name = cmd[1]
        json_data = json.load(open('weapon.json','r'))
        filtered_data = list(filter(lambda x: x["type"]["name"]["ja_JP"] == type_name, json_data))
        if filtered_data:
            buki = random.choice(filtered_data)
            ja_name = buki["name"]["ja_JP"]
            en_name = buki["name"]["en_US"]
            path = "images/main/" + buki["name"]["ja_JP"] + ".png"
            user = message.author.display_name
            await message.channel.send(f"{user}さんにおすすめの{type_name}は{ja_name}({en_name})！" , file=discord.File(path))

    if message.content.lower() in ['gachi', 'ガチ', 'がち', 'gachima', 'ガチマ', 'がちま', 'ガチマッチ', 'がちまっち']:
        key = "ガチマッチ"
        link = "gachi/schedule"
        msg = getStageInfo(link, key)
        await message.channel.send(msg)

    if message.content.lower() in ['league', 'riguma', 'リグマ', 'りぐま', 'リーグマッチ', 'りーぐまっち']:
        key = "リーグマッチ"
        link = "league/schedule"
        msg = getStageInfo(link, key)
        await message.channel.send(msg)

    if message.content.lower() in ['regular', 'レギュラー', 'れぎゅらー', 'レギュラーマッチ', 'れぎゅらーまっち', 'nawabari', 'ナワバリ', 'なわばり', 'ナワバリバトル', 'なわばりばとる']:
        key = "ナワバリバトル"
        link = "regular/schedule"
        msg = getStageInfo(link, key, showRule=False)
        await message.channel.send(msg)

    if message.content.lower() in ['salmon', 'samon', 'sa-mon', 'サーモン', 'さーもん', 'サーモンラン', 'さーもんらん', 'coop', 'コープ', 'こーぷ', 'サケ', 'さけ', 'シャケ', 'しゃけ', '鮭']:
        key = "サーモンラン"
        link = "coop/schedule"
        msg = getCoopInfo(link, key)
        await message.channel.send(msg)

    dice_pattern = '^(?P<dice_num>\d+)d(?P<dice_size>\d+)$' # example: 3d6
    content = message.content.lower()
    match_result = re.match(dice_pattern, content)
    if match_result:
        dice_num = int(match_result.group('dice_num'))
        dice_size = int(match_result.group('dice_size'))
        dice_sum = 0
        for i in range(dice_num):
            dice_sum += random.randint(1, dice_size)
        await message.channel.send(str(dice_sum))

    if client.user in message.mentions: # if mentioned
        if 'おはよ' in message.content:
            msg = "おはようございます！"
            await message.channel.send(msg)
        if 'こんにちは' in message.content:
            msg = "こんにちは！"
            await message.channel.send(msg)
        if 'こんばんは' in message.content:
            msg = "こんばんは！"
            await message.channel.send(msg)
        if 'おやすみ' in message.content:
            msg = "おやすみなさい！"
            await message.channel.send(msg)
        if '好き' in message.content:
            msg = "僕も好き！"
            await message.channel.send(msg)
        if 'たんたん' in message.content:
            msg = "初めましてたんたん麺ですよろしくお願いします！"
            await message.channel.send(msg)
        if 'まそ語録' in message.content:
            with open('maso.txt', 'r') as f:
                maso_list = f.read().split("\n")
            seed = getDailyRandomString() + str(message.author.id)
            random.seed(seed)
            maso_goroku = random.choice(maso_list)
            await message.channel.send(f"今日のまそ語録: {maso_goroku}")

if __name__ == '__main__':
    if "BOT_TOKEN" not in os.environ:
        dotenv_path = join(dirname(__file__), '.env')
        load_dotenv(dotenv_path)
    BOT_TOKEN = os.environ.get("BOT_TOKEN")
    client.run(BOT_TOKEN)
