#MIT License
#Copyright (c) 2020 Semih Aydın
#UTF-8

#EVOS
import discord
from discord.ext import commands
import asyncio
import json
import os

modules = 0
loaded = 0
default_prefix = '.' 

def get_prefix(client,message):
    try :
        with open("./data/ServerData.json", "r") as jsonFile:
            prefixes = json.load(jsonFile)
        return prefixes[str(message.guild.id)]["custom_prefix"]
    except : 
        return default_prefix

def get_token():
    with open("./data/token.json", "r") as tokenjsonFile:
        Data = json.load(tokenjsonFile)
        token = Data["token"]
    return token

client = commands.Bot(command_prefix=get_prefix)

@client.event
async def on_ready():
    print(f'{client.user.name} hazır.')
    print(f"{len(client.guilds)} serverda çalışıyor.")
    await client.change_presence(status=discord.Status.online , activity=discord.Game(f".yardım | 🎵 HIGH QUALITY MUSIC"))

print("Modüller yükleniyor...")
for filename in os.listdir('./cogs'):
    if filename.endswith('.py'):
        modules+=1
        try :
            client.load_extension(f'cogs.{filename[:-3]}')
            print(f"\t{filename[:-3]} yüklendi.")
            loaded+=1
        except :
            print(f"\t{filename[:-3]} yüklenemedi.")
print(f"\t-------------------\n\tToplam Eklenti : \t{modules}\n\tYüklenen Eklenti : \t{loaded}\n\tYüklenemeyen Eklenti : \t{modules-loaded}\n\t-------------------")
print("Modül yükleme işlemi tamamlandı.")

client.run(get_token())