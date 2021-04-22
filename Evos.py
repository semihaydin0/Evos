#MIT License
#Copyright (c) 2020 Semih Aydın
#UTF-8

import discord
from discord.ext import commands
import pyfiglet
import sqlite3
import json
import os
from logging_files.evos_log import logger

intents = discord.Intents.default()
intents.members = True
modules = 0
loaded = 0
defaultPrefix = '.'

def get_prefix(client,message):
    db = sqlite3.connect("data/server/Data.db")
    cursor = db.cursor()
    try :
        cursor.execute("SELECT CUSTOM_PREFIX FROM ServerData WHERE SERVER_ID=?",(str(message.guild.id),))
        customPrefix = cursor.fetchone()
        return customPrefix[0]
    except Exception as e:
        logger.error(f"{client.user.name} | GetPrefix | Error: {e}")
        return defaultPrefix

def get_token():
    with open("data/Token.json", "r") as tokenJsonFile:
        data = json.load(tokenJsonFile)
        token = data["token"]
    return token

def get_version_number():
    with open("data/package.json", "r") as packageJsonFile:
        data = json.load(packageJsonFile)
        versionNumber = data["version"]
    return versionNumber

client = commands.Bot(command_prefix=get_prefix,intents=intents)

@client.event
async def on_ready():
    await client.change_presence(status=discord.Status.online, activity=discord.Activity(type=discord.ActivityType.watching, name=f".yardım | .help | v{get_version_number()}"))
    print(pyfiglet.figlet_format(f"{client.user.name} | v{get_version_number()}"))
    logger.info(f"{client.user.name} is ready.")

print("Modül yükleme işlemi başladı.")
for filename in os.listdir('cogs'):
    if filename.endswith('.py'):
        modules += 1
        try :
            client.load_extension(f'cogs.{filename[:-3]}')
            print(f"\t{filename[:-3]} yüklendi.")
            loaded += 1
        except Exception as e:
            logger.error(f"{client.user.name} | LoadModule | File: {filename[:-3]} | Error: {e}")
            print(f"\t{filename[:-3]} yüklenemedi.")
print(f"\t-------------------------\n\tToplam Eklenti: \t{modules}\n\tYüklenen Eklenti: \t{loaded}\n\tYüklenemeyen Eklenti: \t{modules-loaded}\n\t-------------------------")
print("Modül yükleme işlemi tamamlandı.")

client.run(get_token(), reconnect=True)