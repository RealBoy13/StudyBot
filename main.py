import discord
import os
import requests
import json
import asyncio
import random
import typing
from random import choice
from newspaper import Article
import string
import nltk
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import numpy as np
import warnings
from discord.ext import commands

warnings.filterwarnings('ignore')

client = discord.Client()

a_file = open("אזרחות.txt", "r")
content = a_file.read()
ezrachoot_list = content.split("/")
a_file.close()

a_file = open("מדמח.txt", "r")
content = a_file.read()
mdmh_list = content.split("~")
a_file.close()


@client.event
async def on_ready():
    await client.change_presence(
        activity=discord.Activity(type=discord.ActivityType.watching,
                                  name=' שרת הלימודים הגדול והראשון בישראל! '))
    print('We have logged in as {0.user}'.format(client))


def index_sort(list_var):
    length = len(list_var)
    list_index = list(range(0, length))

    x = list_var
    for i in range(length):
        for j in range(length):
            if x[list_index[i]] > x[list_index[j]]:
                temp = list_index[i]
                list_index[i] = list_index[j]
                list_index[j] = temp

    return list_index


def bot_response(user_input, list):
    sentence_list = list
    user_input = user_input.lower()
    sentence_list.append(user_input)
    bot_response = ''
    cm = CountVectorizer().fit_transform(sentence_list)
    similarity_scores = cosine_similarity(cm[-1], cm)
    similarity_scores_list = similarity_scores.flatten()
    index = index_sort(similarity_scores_list)
    index = index[1:]
    response_flag = 0

    j = 0
    for i in range(len(index)):
        if similarity_scores_list[index[i]] > 0.0:
            bot_response = bot_response + ' ' + sentence_list[index[i]]
            response_flag = 1
            j = j + 1
        if j > 2:
            break

        if response_flag == 0:
            bot_response = bot_response + ' ' + "על מנת לקבל עזרה, תשאל/י שאלה"
        sentence_list.remove(user_input)

        return bot_response


def convert(lst):
    return ([i for item in lst for i in item.split()])


#sad_words = ["עצוב", "דיכאון", "דכאון", "קשה", "מבואס", "מבאס", "בוכה", "רע",  "חרא", "חרא", "בודד", "בדידות", "לבד", "עצבות"]

#alert_words = ["מתעלל", "התעללות", "מתעללת", "להתאבד", "התאבדות", "מתאבד", "אני רוצה למות", "אין תקווה" ,"אין לי תקווה"]

#strange_words = ["שונה", "מוזר", "אחר", "לא משתלב", "משתלב", "השתלבות", "שונות", "זר", "לא שייך", "חוסר שייכות"]

#mental_words = ["חרדה", "חרד", "פחד", "בהלה", "חשש", "חושש", "חוששת", "חוששים", "חוששות"]

#MentalHealth = [""
#]

#def get_Cat():
#  response = requests.get("https://https://aws.random.cat/meow.io/api/random")
# json_data = json.loads(response.text)
# cat = json_data[0]['q'] + " -" + json_data[0]['a']
#return(cat)


def check(m):
    return m.content


@client.event
async def on_message(message):
    if message.author == client.user:
        return

    msg = message.content

    if message.content.startswith('שלום'):
        await message.channel.send('היי :)')

    if message.content.startswith('אזרחות'):
        await message.channel.send(
            bot_response(msg.replace('אזרחות', ''), ezrachoot_list) +
            message.author.mention)

    if message.content.startswith('מחשבון'):
        calculation = eval(msg.replace('מחשבון', ''))
        await message.channel.send(calculation)

    if message.content.startswith('ניתוח מילה'):
        theme = msg.replace('ניתוח מילה', '')
        url = 'https://hebrew-academy.org.il/?s='
        answer = url + theme.strip()
        await message.channel.send(answer)

    if message.content.startswith('סיסמה'):
        await message.channel.send(''.join([
            choice('abcdefghijklmnopqrstuvwxyz0123456789%^*(-_=+)')
            for i in range(15)
        ]))

    if message.content.startswith('מדמח'):
        await message.channel.send(
            bot_response(msg.replace('מדמח', ''), mdmh_list) +
            message.author.mention)

    if message.content.startswith('פעולות עזר'):
        await message.channel.send(
            f'CHARP: https://pastebin.com/dl/7sQHmYLG JAVA: https://pastebin.com/dl/4f7KXDEM  {message.author.mention}'
        )

    if message.content.startswith('קרדיטים'):
        embedVar = discord.Embed(
            title="רשימת הקרדיטים",
            description="הא/נשים והמקומות שעזרו לבנות את הבוט",
            color=0x00ff00)
        embedVar.add_field(name="אתר טקסטולוגיה",
                           value=" https://www.textologia.net ",
                           inline=False)
        embedVar.add_field(
            name="הילה קדמן",
            value=" http://blog.csit.org.il/MyBlog.aspx?BlogID=33 ",
            inline=False)
        embedVar.add_field(name="זוהר יחיא",
                           value=" @RealBoy#1649 ",
                           inline=False)
        embedVar.add_field(name=" Saurik ",
                           value=" https://www.fxp.co.il/member.php?u=747190 ",
                           inline=False)
        await message.channel.send(embed=embedVar)

    if message.content.startswith('פקודות'):
        embedVar = discord.Embed(
            title="רשימת הפקודות",
            description=
            "רשמו את הפקודה ולאחריה את .מה שבסוגריים. אם אין סוגריים רק את הפקודה)",
            color=0x00ff00)
        embedVar.add_field(name="סיכומים באזרחות",
                           value=" אזרחות __(נושא)",
                           inline=False)
        embedVar.add_field(name="מחשבון",
                           value="  מחשבון __(תרגיל)",
                           inline=False)
        embedVar.add_field(name="ניתוח מילה",
                           value="  ניתוח מילה __(מילה)",
                           inline=False)
        embedVar.add_field(name="סיכומים במדעי המחשב ",
                           value="  מדמח __(נושא)",
                           inline=False)
        embedVar.add_field(name="פעולות עזר במדעי המחשב ",
                           value="פעולות עזר",
                           inline=False)
        embedVar.add_field(name="סיסמה", value="  סיסמה ", inline=False)
        embedVar.add_field(
            name="קרדיטים על סיכומים",
            value="  קרדיטים  ",
            inline=False)

        await message.channel.send(embed=embedVar)


client.run('ODUwODIwMjE4MDQwMDkwNjY1.YLvSEw.lMSginnb6tR8NDwJo5nvtJlWjcQ')
