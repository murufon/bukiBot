# coding: UTF-8
import discord
import logging

import os
from os.path import join, dirname
from dotenv import load_dotenv

import json
import random

import datetime

import requests

logging.basicConfig(level=logging.INFO)

client = discord.Client()

@client.event
async def on_ready():
    print('-----')
    print('logged in')
    print(f"user name: {client.user.name}")
    print(f"user id: {client.user.id}")
    print('-----')

@client.event
async def on_message(message):
    # メッセージ送信者がBotだった場合は無視する
    if message.author.bot:
        return

    if message.content.lower() in ['buki', 'ぶき', 'ブキ', '武器', 'weapon', 'うえぽん', 'ウエポン', 'arms', 'アームズ', 'あーむず']:
        json_data = json.load(open('weapon.json','r'))
        buki = random.choice(json_data)
        ja_name = buki["name"]["ja_JP"]
        en_name = buki["name"]["en_US"]
        path = "images/main/" + buki["name"]["ja_JP"] + ".png"
        user = message.author.display_name
        await message.channel.send(f"{user}さんにおすすめのブキは{ja_name}({en_name})！" , file=discord.File(path))
    
    if message.content.lower() in ['gachi', 'ガチ', 'がち', 'gachima', 'ガチマ', 'がちま', 'ガチマッチ', 'がちまっち']:
        headers = {"User-Agent": "@murufon"}
        url = "https://spla2.yuu26.com/" + "gachi/schedule"
        response = requests.get(url,headers=headers)
        json_data = json.loads(response.text)
        r = json_data['result']
        time_format = '%Y-%m-%dT%H:%M:%S'
        msg = "ガチマッチのスケジュールはこちら！\n"
        msg += "```\n"
        for i in range(3):
            start = datetime.datetime.strptime(r[i]['start'], time_format)
            end = datetime.datetime.strptime(r[i]['end'], time_format)
            msg += "\n"
            msg += f"{start.hour}時〜{end.hour}時\n"
            msg += f"{r[i]['rule']}\n"
            msg += f"{r[i]['maps'][0]}/{r[i]['maps'][1]}\n"
        msg += "```\n"
        await message.channel.send(msg)



if __name__ == '__main__':
    if "BOT_TOKEN" not in os.environ:
        dotenv_path = join(dirname(__file__), '.env')
        load_dotenv(dotenv_path)
    BOT_TOKEN = os.environ.get("BOT_TOKEN")
    client.run(BOT_TOKEN)
