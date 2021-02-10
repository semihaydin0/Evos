#MIT License
#Copyright (c) 2020 Semih Aydın
#UTF-8

import discord
from discord.ext import tasks, commands
import asyncio
import sqlite3
from logging_files.events_log import logger

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
        
        db = sqlite3.connect('data/server/Config.db')
        cursor = db.cursor()
        try :
            cursor.execute("UPDATE AutoMessage SET TIME_LEFT=TIME_LEFT-1")
            db.commit()
        except Exception as e :
            logger.error(f"Events | AutoMessageTimeOrganizer | Error: {e}")
        finally :
            cursor.close()
            db.close()

    @tasks.loop(minutes=1)
    async def muted_users_time_organizer(self):
        await self.client.wait_until_ready()
        
        db = sqlite3.connect('data/server/Mute.db')
        cursor = db.cursor()
                    
        try :
            cursor.execute("UPDATE MutedUsers SET TIME_LEFT = TIME_LEFT-1")
            db.commit()
        except Exception as e :
            logger.error(f"Events | MutedUsersTimeOrganizer | Error: {e}")
        finally :
            cursor.close()
            db.close()

    @tasks.loop(hours=1)
    async def auto_message(self):
        await self.client.wait_until_ready()
        await asyncio.sleep(15)
        
        db = sqlite3.connect('data/server/Config.db')
        cursor = db.cursor()
        
        try :
            cursor.execute("SELECT CHANNEL_ID,MESSAGE_CONTENT FROM AutoMessage WHERE TIME_LEFT <= 0")
            data = cursor.fetchall()
            db.commit()
            
            for guild in self.client.guilds :
                
                for _data in data :
                    
                    for channel in guild.text_channels :
                        
                        if str(channel.id) == _data[0] :
                            
                            try :
                                channelID = discord.utils.get(guild.text_channels, id=int(channel.id))
                                messageContent = _data[1]
                            
                                await channelID.send(messageContent)
                                
                                cursor.execute("UPDATE AutoMessage SET TIME_LEFT = DEFAULT_TIME WHERE TIME_LEFT <= 0")
                                db.commit()
                            except Exception as e :
                                logger.error(f"Events | AutoMessage-2 | Error: {e}")
        except Exception as e :
            logger.error(f"Events | AutoMessage-1 | Error: {e}")
        finally :
            cursor.close()
            db.close()                

    @tasks.loop(minutes=1)
    async def unmute_organizer(self):
        await self.client.wait_until_ready()
        await asyncio.sleep(10)
        
        db = sqlite3.connect('data/server/Mute.db')
        cursor = db.cursor()
        
        try :
            cursor.execute("SELECT USER_ID FROM MutedUsers WHERE TIME_LEFT <= 0")
            users = cursor.fetchall()
            db.commit()
            
            for guild in self.client.guilds :
                role = discord.utils.get(guild.roles,name = "Muted")
                
                for user in users :
                    
                    for member in guild.members :
                        
                        if str(member.id) == user[0] :
                            
                            try :
                                await member.remove_roles(role)
                                cursor.execute("DELETE FROM MutedUsers WHERE USER_ID=?",(user[0],))
                                db.commit()
                            except Exception as e :
                                logger.error(f"Events | UnmuteOrganizer-2 | Error: {e}")
        except Exception as e :
            logger.error(f"Events | UnmuteOrganizer-1 | Error: {e}")
        finally :
            cursor.close()
            db.close()

def setup(client):
    client.add_cog(Events(client))