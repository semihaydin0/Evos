#MIT License
#Copyright (c) 2020 Semih Aydın
#UTF-8

#Warning: Most of these commands will not work if your bot is an unverified bot.
#More Information : https://blog.discord.com/the-future-of-bots-on-discord-4e6e050ab52e

import discord
from discord.utils import get
from discord.ext import commands
import json
import asyncio

from logging_files.guild_log import logger

dataSource = "./data/ServerData.json"

def check_channel(author,channel):
    def inner_check(message):
        return len(message.channel_mentions) == 1 and message.author == author and message.channel.id == channel

    return inner_check

def check_autorole(author,channel):
    def inner_check(message):
        return len(message.role_mentions) == 1 and message.author == author and message.channel.id == channel
    
    return inner_check

def check_prefix(author,channel):
    def inner_check(message):
        return len(message.content) <= 3 and message.author == author and message.channel.id == channel
    
    return inner_check
    
class Guild(commands.Cog):
    def __init__(self,client):
        self.client = client

    @commands.command(name = "Wlmesaj",brief = "Sunucuna gelen yeni üyeler için karşılama mesajı gönderir.",aliases = ["wlmesaj"])
    @commands.has_permissions(administrator=True)
    async def member_welcome_command(self,ctx):
        """Welcome message for newcomers
        Use of : wlmesaj
        """
        await ctx.send(f"Selam {ctx.author.mention} !\nBu komut için seçmek istediğin kanalı belirleyelim.\n`Belirlemek istediğin kanalı etiketlemen yeterli.`")
        
        try:
            channelSelection = await self.client.wait_for('message',check = check_channel(ctx.author,ctx.message.channel.id) ,timeout=30)
        except asyncio.TimeoutError:
            await ctx.send(f"zZ:sleeping:Zz {ctx.author.mention} Maalesef senden herhangi bir yanıt alamadık.")
        
        else :
            try :
                channel_id = channelSelection.channel_mentions[0].id
                jsonFile = open(dataSource, "r")
                data = json.load(jsonFile)
                jsonFile.close()
                data[str(ctx.author.guild.id)]["welcome_channel_id"] = channel_id
                with open (dataSource, 'w+') as f:
                    json.dump(data, f,indent=4)
                await ctx.send(f"Harika :partying_face: ! Artık {channelSelection.channel_mentions[0].mention} kanalında yeni üyeler için bilgilendirme mesajı gönderilecek.")
                logger.info(f"Guild | Wlmesaj | Sunucu : {ctx.guild.name} | Tarafından : {ctx.author}")
            except Exception as error:
                await ctx.send(":thinking: Görünüşe göre şu anda sunucu kayıtlarına ulaşamıyoruz.Daha sonra tekrar deneyebilirsin.")
                
                logger.info(f"Guild | Wlmesaj | Error : {error}")

    @commands.command(name = "Lvmesaj",brief = "Sunucundan ayrılan üyeler için ayrılma mesajı gönderir.",aliases = ["lvmesaj"])
    @commands.has_permissions(administrator=True)
    async def member_leave_command(self,ctx):
        """Information message for leaving members
        Use of : lvmesaj
        """
        await ctx.send(f"Selam {ctx.author.mention} !\nBu komut için seçmek istediğin kanalı belirleyelim.\n`Belirlemek istediğin kanalı etiketlemen yeterli.`")

        try:
            channelSelection = await self.client.wait_for('message',check = check_channel(ctx.author,ctx.message.channel.id) ,timeout=30)
        except asyncio.TimeoutError:
            await ctx.send(f"zZ:sleeping:Zz {ctx.author.mention} Maalesef senden herhangi bir yanıt alamadık.")

        else :
            try :
                channel_id = channelSelection.channel_mentions[0].id
                jsonFile = open(dataSource, "r")
                data = json.load(jsonFile)
                jsonFile.close()
                data[str(ctx.author.guild.id)]["leave_channel_id"] = channel_id
                with open (dataSource, 'w+') as f:
                    json.dump(data, f,indent=4)
                await ctx.send(f"Harika :partying_face: ! Artık {channelSelection.channel_mentions[0].mention} kanalında ayrılan üyeler için bilgilendirme mesajı gönderilecek.")
                logger.info(f"Guild | Lvmesaj | Sunucu : {ctx.guild.name} | Tarafından : {ctx.author}")
            except Exception as error:
                await ctx.send(":thinking: Görünüşe göre şu anda sunucu kayıtlarına ulaşamıyoruz.Daha sonra tekrar deneyebilirsin.")

                logger.info(f"Guild | Lvmesaj | Error : {error}")

    @commands.command(name = "SetAutorole",brief = "Sunucundan gelen üyeler için otomatik rol verir.",aliases = ["setautorole"])
    @commands.has_permissions(administrator=True)
    async def autorole_command(self,ctx):
        """Automatic role for newcomers
        Use of : setautorole
        """
        await ctx.send(f"Selam {ctx.author.mention} !\nBu komut için seçmek istediğin rolü belirleyelim.\n`Belirlemek istediğin rolü etiketlemen yeterli.`")
        
        try:
            roleSelection = await self.client.wait_for('message',check = check_autorole(ctx.author,ctx.message.channel.id) ,timeout=30)
        except asyncio.TimeoutError:
            await ctx.send(f"zZ:sleeping:Zz {ctx.author.mention} Maalesef senden herhangi bir yanıt alamadık.")
        
        else :
            try :
                role_id = roleSelection.role_mentions[0].id
                jsonFile = open(dataSource, "r")
                data = json.load(jsonFile)
                jsonFile.close()
                data[str(ctx.author.guild.id)]["autorole_id"] = role_id
                with open (dataSource, 'w+') as f:
                    json.dump(data, f,indent=4)
                await ctx.send(f"Harika :partying_face: ! Artık yeni gelen üyelere otomatik olarak {roleSelection.role_mentions[0].mention} rolü verilecek.\n`Uyarı : Evos'un bu işlevi tam olarak yerine getirebilmesi için roller kısmından Evos'un rolünü {roleSelection.role_mentions[0]} rolünden en az 1 kademe üstüne taşıman gerekli.`")
                logger.info(f"Guild | Autorole | Sunucu : {ctx.guild.name} | Tarafından : {ctx.author}")
            except Exception as error:
                await ctx.send(":thinking: Görünüşe göre şu anda sunucu kayıtlarına ulaşamıyoruz.Daha sonra tekrar deneyebilirsin.")
                
                logger.info(f"Guild | Autorole | Error : {error}")

    @commands.command(name = "ChangePrefix",brief = "Evos'un komut ön ekini sunucuya özel olarak değiştirir.",aliases = ["changeprefix"])
    @commands.has_permissions(administrator=True)
    async def change_prefix_command(self,ctx):
        """Change prefix
        Use of : changeprefix
        """
        await ctx.send(f"Selam {ctx.author.mention} !\nBu komut için seçmek istediğin prefix'i belirleyelim.\n`Maksimum 3 karakter olmasını ve son karakterinde işaret bulundurmanızı öneriyoruz.`")
        
        try:
            prefixSelection = await self.client.wait_for('message',check = check_prefix(ctx.author,ctx.message.channel.id) ,timeout=30)
        except asyncio.TimeoutError:
            await ctx.send(f"zZ:sleeping:Zz {ctx.author.mention} Maalesef senden herhangi bir yanıt alamadık.")
        
        else :
            try :
                jsonFile = open(dataSource, "r")
                data = json.load(jsonFile)
                jsonFile.close()
                data[str(ctx.author.guild.id)]["custom_prefix"] = prefixSelection.content
                with open (dataSource, 'w+') as f:
                    json.dump(data, f,indent=4)
                await ctx.send(f"Harika :partying_face: ! Artık Evos'un bu sunucu için komut ön eki **{prefixSelection.content}** olarak ayarlandı.")
                logger.info(f"Guild | Prefix | Sunucu : {ctx.guild.name} | Tarafından : {ctx.author}")
            except Exception as error:
                await ctx.send(":thinking: Görünüşe göre şu anda sunucu kayıtlarına ulaşamıyoruz.Daha sonra tekrar deneyebilirsin.")
                
                logger.info(f"Guild | Prefix | Error : {error}")

    @commands.command(name = "ResetConfig",brief = "Sunucu için ayarlanmış olan tüm bilgileri siler.",aliases = ["resetconfig"])
    @commands.has_permissions(administrator=True)
    async def serverdata_reset_command(self,ctx):
        """Reset Server Data
        Use of : resetconfig
        """
        try :
            jsonFile = open(dataSource, "r")
            data = json.load(jsonFile)
            jsonFile.close()
            data[str(ctx.author.guild.id)] = {}
            data[str(ctx.author.guild.id)]["custom_prefix"] = "."
            with open (dataSource, 'w+') as f:
                json.dump(data, f,indent=4)
            await ctx.send(f"Harika :partying_face: ! Bu sunucunun tüm ayarları sıfırlandı.Evos'un komut ön eki varsayılan(**.(nokta)**) olarak ayarlandı.")
        except Exception as error:
                await ctx.send(":thinking: Görünüşe göre şu anda sunucu kayıtlarına ulaşamıyoruz.Daha sonra tekrar deneyebilirsin.")
                
                logger.info(f"Guild | Svreset | Error : {error}")

    @commands.Cog.listener()
    async def on_member_join(self,member):
        status = False
        auto = False
        wlchn = False
        
        try :
            jsonFile = open(dataSource, "r")
            ServerData = json.load(jsonFile)
            jsonFile.close()
            status = True
        except Exception as error:

            logger.info(f"Guild | Data | Error : {error}")
            pass
        
        if status==True and member.name!=self.client.user.name :
            
            try : 
                autorole_id = ServerData[str(member.guild.id)]['autorole_id']
                auto = True
            except :
                pass
            
            try :    
                wlchannel_id = ServerData[str(member.guild.id)]['welcome_channel_id']
                wlchn = True
            except :
                pass
            
            if auto == True :
                autorole = discord.utils.get(member.guild.roles, id=int(autorole_id))
                
                if autorole != None :
                    
                    try :
                        await member.add_roles(autorole)
                    except :
                        pass
            
            if wlchn == True :
                wlchannel = discord.utils.get(member.guild.text_channels, id=int(wlchannel_id))
                
                if wlchannel != None :
                    welcomeEmbed = discord.Embed(title = "Bir yeni üye daha !",description = f"Aramıza hoşgeldin {member.mention} !",colour=0xd8f500)
                    welcomeEmbed.set_author(name=member.guild.name,icon_url=member.guild.icon_url)
                    welcomeEmbed.set_thumbnail(url=member.avatar_url)
                    file = discord.File("images/evos.png", filename="evos.png")
                    welcomeEmbed.set_footer(text=f"{len(member.guild.members)}.Üye",icon_url="attachment://evos.png")
                    
                    await wlchannel.send(file=file,embed=welcomeEmbed) 
        else :
            pass

    @commands.Cog.listener()
    async def on_member_remove(self,member):
        status = False
        lvchn = False
        
        try :
            jsonFile = open(dataSource, "r")
            ServerData = json.load(jsonFile)
            jsonFile.close()
            status = True
        except Exception as error:

            logger.info(f"Guild | Data | Error : {error}")
            pass
        
        if status==True and member.name!=self.client.user.name :
            
            try :    
                lvchannel_id = ServerData[str(member.guild.id)]['leave_channel_id']
                lvchn = True
            except :
                pass
        
        if lvchn == True :
            lvchannel = discord.utils.get(member.guild.text_channels, id=int(lvchannel_id))
            
            if lvchannel != None :
                leaveEmbed = discord.Embed(title = "Aramızdan birisi eksildi !",description = f"{member.mention} Aramızdan ayrıldı !",colour=0xd8f500)
                leaveEmbed.set_author(name=member.guild.name,icon_url=member.guild.icon_url)
                leaveEmbed.set_thumbnail(url=member.avatar_url)
                file = discord.File("images/evos.png", filename="evos.png")
                leaveEmbed.set_footer(text=f"{len(member.guild.members)} Üye",icon_url="attachment://evos.png")
                
                await lvchannel.send(file=file,embed=leaveEmbed)
            else :
                pass     
        else : 
            pass


    @commands.Cog.listener()
    async def on_guild_join(self, guild):
        try :
            jsonFile = open(dataSource, "r")
            data = json.load(jsonFile)
            jsonFile.close()
            data[str(guild.id)] = {}
            data[str(guild.id)]["custom_prefix"] = "."
            
            with open (dataSource, 'w+') as f:
                json.dump(data, f,indent=4)
        except Exception as error:

            logger.info(f"Guild | OnGuildJoin-Data | Error : {error}")
            pass

def setup(client):
    client.add_cog(Guild(client))