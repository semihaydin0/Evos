#MIT License
#Copyright (c) 2020 Semih Aydın
#UTF-8

import discord
from discord.utils import get
from discord.ext import tasks, commands
import asyncio
import json

dataSource = "./data/server/ServerConfig.json"
dataSource2 = "./data/server/MuteList.json"
configStatus = False
listStatus = False
currentTimeLeft = 0
currentTimeLeft2 = 0
defaultTime = 0

class Events(commands.Cog):
    def __init__(self,client):
        self.client = client
        self.auto_message_time_organizer.start()
        self.muted_users_time_organizer.start()
        self.auto_message.start()
        self.unmute_organizer.start()
    
    @tasks.loop(hours=1)
    async def auto_message_time_organizer(self):
        await self.client.wait_until_ready()
        
        try :
            jsonFile = open(dataSource, "r")
            svConfig = json.load(jsonFile)
            jsonFile.close()
            configStatus = True
        except :
            configStatus = False
            pass
        
        if configStatus == True:
            for guild in self.client.guilds:
                for channel in guild.text_channels:
                    
                    try :
                        currentTimeLeft = svConfig[str(channel.id)]['auto_message_timer']
                        defaultTime = svConfig[str(channel.id)]['default_time']
                        if currentTimeLeft > 0 :
                            
                            if currentTimeLeft - 1 == 0 :
                                svConfig[str(channel.id)]['auto_message_timer'] = svConfig[str(channel.id)]['default_time']
                            else :
                                svConfig[str(channel.id)]['auto_message_timer'] = currentTimeLeft - 1
                        elif defaultTime > 0:
                            svConfig[str(channel.id)]['auto_message_timer'] = svConfig[str(channel.id)]['default_time']
                        with open (dataSource, 'w+') as f:
                            json.dump(svConfig, f,indent=4)    
                    except :
                        pass

    @tasks.loop(minutes=1)
    async def muted_users_time_organizer(self):
        await self.client.wait_until_ready()
        
        try :
            jsonFile = open(dataSource2, "r")
            muteList = json.load(jsonFile)
            jsonFile.close()
            listStatus = True
        except :
            listStatus = False
            pass
        
        if listStatus == True:
            for guild in self.client.guilds:
                for member in guild.members:
                    
                    try :
                        currentTimeLeft2 = muteList[str(member.id)]['TIME_LEFT']
                        
                        if currentTimeLeft2 > 0 :
                            muteList[str(member.id)]['TIME_LEFT'] = currentTimeLeft2 - 1
                        
                        with open (dataSource2, 'w+') as f:
                            json.dump(muteList, f,indent=4)
                    except :
                        pass
    
    @tasks.loop(hours=1)
    async def auto_message(self):
        await self.client.wait_until_ready()
        
        await asyncio.sleep(60)
        try :
            jsonFile = open(dataSource, "r")
            svConfig = json.load(jsonFile)
            jsonFile.close()
            configStatus = True
        except :
            configStatus = False
            pass
        
        if configStatus == True:
            for guild in self.client.guilds:
                for channel in guild.text_channels:
                    
                    try :
                        currentTimeLeft = svConfig[str(channel.id)]['auto_message_timer']
                        defaultTime = svConfig[str(channel.id)]['default_time']
                        
                        if defaultTime == currentTimeLeft :
                            automessage_channel_id = discord.utils.get(guild.text_channels, id=int(channel.id))
                            automessage_text = svConfig[str(channel.id)]['auto_message_text']
                            
                            await automessage_channel_id.send(automessage_text)
                    except :
                        pass

    @tasks.loop(minutes=1)
    async def unmute_organizer(self):
        await self.client.wait_until_ready()
        
        await asyncio.sleep(10)
        try :
            jsonFile = open(dataSource2, "r")
            muteList = json.load(jsonFile)
            jsonFile.close()
            listStatus = True
        except :
            listStatus = False
            pass
        
        if listStatus == True:
            for guild in self.client.guilds:
                for member in guild.members:
                    
                    try :
                        currentTimeLeft2 = muteList[str(member.id)]['TIME_LEFT']
                        
                        if currentTimeLeft2 == 0:
                            role = discord.utils.get(guild.roles,name = "Muted")
                            
                            try :
                                await member.remove_roles(role)
                                
                                muteList[str(member.id)]['TIME_LEFT'] = -1
                                
                                with open (dataSource2, 'w+') as f:
                                    json.dump(muteList, f,indent=4)
                            except :
                                pass
                    except :
                        pass

def setup(client):
    client.add_cog(Events(client))