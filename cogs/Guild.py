#MIT License
#Copyright (c) 2020 Semih Aydın
#UTF-8

import discord
from discord.utils import get
from discord.ext import commands
import json
import asyncio
from logging_files.guild_log import logger

dataSource = "./data/server/ServerData.json"
dataSource_2 = "./data/server/ServerConfig.json"

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

def check_message(author,channel):
    def inner_check(message):
        return message.author == author and message.channel.id == channel

    return inner_check
    
class Guild(commands.Cog):
    def __init__(self,client):
        self.client = client

    @commands.command(name = "Wlmessage",brief = "Sunucuna gelen yeni üyeler için karşılama mesajı gönderir.",aliases = ["wlmessage"])
    @commands.has_permissions(administrator=True)
    async def member_welcome_command(self,ctx):
        """Welcome message for newcomers
        Use of : wlmessage
        """
        await ctx.send(f"Selam {ctx.author.mention}!\nSeçmek istediğin kanalı belirleyelim.\n`Belirlemek istediğin kanalı etiketlemen yeterli.`") 
        
        try:
            channelSelection = await self.client.wait_for('message',check = check_channel(ctx.author,ctx.message.channel.id) ,timeout=30)
        except asyncio.TimeoutError:
            await ctx.send(f":sleeping: {ctx.author.mention} Belirlenen sürede senden herhangi bir yanıt alamadık.")
        
        else :
            try :
                channelID = channelSelection.channel_mentions[0].id
                jsonFile = open(dataSource, "r")
                data = json.load(jsonFile)
                jsonFile.close()
                data[str(ctx.author.guild.id)]["WELCOME_CHANNEL_ID"] = channelID
                
                with open (dataSource, 'w+') as f:
                    json.dump(data, f,indent=4)
                
                await ctx.send(f"Harika! :partying_face: Artık {channelSelection.channel_mentions[0].mention} kanalında yeni üyeler için bilgilendirme mesajı gönderilecek.")
                
                logger.info(f"Guild | Wlmessage | Sunucu : {ctx.guild.name} | Tarafından : {ctx.author}")
            except Exception as error:
                await ctx.send(":thinking: Görünüşe göre şu anda sunucu kayıtlarına ulaşamıyoruz.Daha sonra tekrar deneyebilirsin.")         
                
                logger.info(f"Guild | Wlmessage | Error : {error}")

    @commands.command(name = "Lvmessage",brief = "Sunucundan ayrılan üyeler için ayrılma mesajı gönderir.",aliases = ["lvmessage"])
    @commands.has_permissions(administrator=True)
    async def member_leave_command(self,ctx):
        """Information message for leaving members
        Use of : lvmessage
        """
        await ctx.send(f"Selam {ctx.author.mention}!\nSeçmek istediğin kanalı belirleyelim.\n`Belirlemek istediğin kanalı etiketlemen yeterli.`")
        
        try:
            channelSelection = await self.client.wait_for('message',check = check_channel(ctx.author,ctx.message.channel.id) ,timeout=30)
        except asyncio.TimeoutError:
            await ctx.send(f":sleeping: {ctx.author.mention} Belirlenen sürede senden herhangi bir yanıt alamadık.")
        
        else :
            try :
                channelID = channelSelection.channel_mentions[0].id
                jsonFile = open(dataSource, "r")
                data = json.load(jsonFile)
                jsonFile.close()
                data[str(ctx.author.guild.id)]["LEAVE_CHANNEL_ID"] = channelID
                
                with open (dataSource, 'w+') as f:
                    json.dump(data, f,indent=4)
                
                await ctx.send(f"Harika! :partying_face: Artık {channelSelection.channel_mentions[0].mention} kanalında ayrılan üyeler için bilgilendirme mesajı gönderilecek.")
                
                logger.info(f"Guild | Lvmessage | Sunucu : {ctx.guild.name} | Tarafından : {ctx.author}")
            except Exception as error:
                await ctx.send(":thinking: Görünüşe göre şu anda sunucu kayıtlarına ulaşamıyoruz.Daha sonra tekrar deneyebilirsin.")
                
                logger.info(f"Guild | Lvmessage | Error : {error}")
                pass

    @commands.command(name = "Setautorole",brief = "Sunucundan gelen üyeler için otomatik rol verir.",aliases = ["setautorole"])
    @commands.has_permissions(administrator=True)
    async def autorole_command(self,ctx):
        """Automatic role for newcomers
        Use of : setautorole
        """
        await ctx.send(f"Selam {ctx.author.mention}!\nSeçmek istediğin rolü belirleyelim.\n`Belirlemek istediğin rolü etiketlemen yeterli.`")      
        
        try:
            roleSelection = await self.client.wait_for('message',check = check_autorole(ctx.author,ctx.message.channel.id) ,timeout=30)
        except asyncio.TimeoutError:
            await ctx.send(f":sleeping: {ctx.author.mention} Belirlenen sürede senden herhangi bir yanıt alamadık.")
        else :
            try :
                roleID = roleSelection.role_mentions[0].id
                jsonFile = open(dataSource, "r")
                data = json.load(jsonFile)
                jsonFile.close()
                data[str(ctx.author.guild.id)]["AUTOROLE_ID"] = roleID
                
                with open (dataSource, 'w+') as f:
                    json.dump(data, f,indent=4)
                
                await ctx.send(f"Harika! :partying_face: Artık yeni gelen üyelere {roleSelection.role_mentions[0].mention} rolü verilecek.\n`Uyarı: Evos'un bu işlevi tam olarak yerine getirebilmesi için roller kısmından Evos'un rolünü {roleSelection.role_mentions[0]} rolünden en az 1 kademe üstüne taşıman gerekli.`")
                
                logger.info(f"Guild | Autorole | Sunucu : {ctx.guild.name} | Tarafından : {ctx.author}")
            except Exception as error:
                await ctx.send(":thinking: Görünüşe göre şu anda sunucu kayıtlarına ulaşamıyoruz.Daha sonra tekrar deneyebilirsin.")             
                
                logger.info(f"Guild | Autorole | Error : {error}")
                pass

    @commands.command(name = "ChangePrefix",brief = "Evos'un komut ön ekini değiştirir.",aliases = ["changeprefix"])
    @commands.has_permissions(administrator=True)
    async def change_prefix_command(self,ctx):
        """Change Prefix
        Use of : changeprefix
        """
        await ctx.send(f"Selam {ctx.author.mention}!\nSeçmek istediğin komut ön ekini belirleyelim.\n`Maksimum 3 karakter olmasını ve son karakterinde işaret bulundurmanızı öneriyoruz.`")     
        
        try:
            prefixSelection = await self.client.wait_for('message',check = check_prefix(ctx.author,ctx.message.channel.id) ,timeout=60)
        except asyncio.TimeoutError:
            await ctx.send(f":sleeping: {ctx.author.mention} Belirlenen sürede senden herhangi bir yanıt alamadık.")
        else :
            try :
                jsonFile = open(dataSource, "r")
                data = json.load(jsonFile)
                jsonFile.close()
                data[str(ctx.author.guild.id)]["CUSTOM_PREFIX"] = prefixSelection.content
                
                with open (dataSource, 'w+') as f:
                    json.dump(data, f,indent=4)
                
                await ctx.send(f"Harika! :partying_face: Bu sunucu için komut ön eki **{prefixSelection.content}** olarak ayarlandı.")
                
                logger.info(f"Guild | Prefix | Sunucu : {ctx.guild.name} | Tarafından : {ctx.author}")
            except Exception as error:
                await ctx.send(":thinking: Görünüşe göre şu anda sunucu kayıtlarına ulaşamıyoruz.Daha sonra tekrar deneyebilirsin.")            
                
                logger.info(f"Guild | Prefix | Error : {error}")
                pass

    @commands.command(name = "ResetConfig",brief = "Sunucu ayarlarını sıfırlar.",aliases = ["resetconfig"])
    @commands.has_permissions(administrator=True)
    async def server_config_reset_command(self,ctx):
        """Reset Server Config
        Use of : resetconfig
        """
        try :
            jsonFile = open(dataSource, "r")
            data = json.load(jsonFile)
            jsonFile.close()
            data[str(ctx.author.guild.id)] = {}
            data[str(ctx.author.guild.id)]["CUSTOM_PREFIX"] = "."
            
            with open (dataSource, 'w+') as f:
                json.dump(data, f,indent=4)           
            jsonFile = open(dataSource_2, "r")
            ServerConfig = json.load(jsonFile)
            jsonFile.close()
            
            for channel in ctx.message.guild.channels :
                try :
                    temp = ServerConfig[str(channel.id)]['TEXT']
                    ServerConfig[str(channel.id)] = {}
                    ServerConfig[str(channel.id)]["TEXT"] = "DELETED CONTENT"
                    ServerConfig[str(channel.id)]["TIMER"] = 0
                    ServerConfig[str(channel.id)]["DEFAULT"] = -1
                except :
                    pass
            
            with open (dataSource_2, 'w+') as f:
                json.dump(ServerConfig, f,indent=4)
            
            await ctx.send(f"Harika! :partying_face: Bu sunucunun tüm ayarları sıfırlandı. Prefix(komut ön eki) varsayılan **.(nokta)** olarak ayarlandı.")
        except Exception as error:
                await ctx.send(":thinking: Görünüşe göre şu anda sunucu kayıtlarına ulaşamıyoruz.Daha sonra tekrar deneyebilirsin.")               
                
                logger.info(f"Guild | ResetServerConfig | Error : {error}")
                pass

    @commands.command(name = "Automessage",brief = "İstediğiniz kanalde istediğiniz mesajı otomatik gönderir.",aliases = ["automessage",'otomesaj'])
    @commands.has_permissions(administrator=True)
    async def auto_message_scheduler_command(self,ctx):
        """Auto Message Scheduler
        Use of : automessage
        """
        await ctx.send(f"Selam {ctx.author.mention}!\nÖnce istediğin duyurmak istediğin mesajı belirleyelim.\n`Mesajının maksimum 512 karakter olmasını öneriyoruz.`")     
        
        try:
            messageSelection = await self.client.wait_for('message',check = check_message(ctx.author,ctx.message.channel.id) ,timeout=300)
        except asyncio.TimeoutError:
            await ctx.send(f":sleeping: {ctx.author.mention} Belirlenen sürede senden herhangi bir yanıt alamadık.")
        
        else :
            await ctx.send(f"Harika! :partying_face: Şimdi bu mesajın kaç saatte bir yayınlanmasını gerektiğini belirleyelim.\n`Sadece tam sayı girişi yapman gerekir. Aksi taktirde bu sistem çalışmayacaktır.`")           
            
            try:
                timeSelection = await self.client.wait_for('message',check = check_message(ctx.author,ctx.message.channel.id) ,timeout=30)
            except asyncio.TimeoutError:
                await ctx.send(f":sleeping: {ctx.author.mention} Belirlenen sürede senden herhangi bir yanıt alamadık.")
            
            else :          
                try :
                    jsonFile = open(dataSource_2, "r")
                    ServerConfig = json.load(jsonFile)
                    jsonFile.close()
                    ServerConfig[str(ctx.message.channel.id)] = {}
                    ServerConfig[str(ctx.message.channel.id)]["TEXT"] = messageSelection.content
                    ServerConfig[str(ctx.message.channel.id)]["TIMER"] = int(timeSelection.content)
                    ServerConfig[str(ctx.message.channel.id)]["DEFAULT"] = int(timeSelection.content)                 
                    
                    with open (dataSource_2, 'w+') as f:
                        json.dump(ServerConfig, f,indent=4)
                    
                    await ctx.send(f"Harika! :partying_face: Artık bu kanalda her **{timeSelection.content}** saatte bir mesajın yayınlanacak.")             
                    
                    logger.info(f"Guild | AutoMessage | Sunucu : {ctx.guild.name} | Mesaj : {messageSelection.content} |Tarafından : {ctx.author}")
                except Exception as error:
                    await ctx.send(":thinking: Görünüşe göre şu anda sunucu kayıtlarına ulaşamıyoruz.Daha sonra tekrar deneyebilirsin.")              
                    
                    logger.info(f"Guild | AutoMessage | Error : {error}")
                    pass

    @commands.Cog.listener()
    async def on_member_join(self,member):
        autoRoleStatus = False
        channelStatus = False
        
        try :
            jsonFile = open(dataSource, "r")
            ServerData = json.load(jsonFile)
            jsonFile.close()
            
            try :
                autoRoleID = ServerData[str(member.guild.id)]['AUTOROLE_ID']
                autoRoleStatus = True
            except :
                pass
            
            try :
                channelID = ServerData[str(member.guild.id)]['WELCOME_CHANNEL_ID']
                channelStatus = True
            except :
                pass
            
            if autoRoleStatus == True :
                autoRole = discord.utils.get(member.guild.roles, id=int(autoRoleID))
                
                if autoRole != None :                  
                    try :
                        await member.add_roles(autoRole)
                    except :
                        pass
            
            if channelStatus == True :
                channel = discord.utils.get(member.guild.text_channels, id=int(channelID))
                
                if channel != None :
                    welcomeEmbed = discord.Embed(title = "Bir yeni üye daha !",description = f"Aramıza hoşgeldin {member.mention} !",colour=0xd8f500)
                    welcomeEmbed.set_author(name=member.guild.name,icon_url=member.guild.icon_url)
                    welcomeEmbed.set_thumbnail(url=member.avatar_url)
                    file = discord.File("images/evos.png", filename="evos.png")
                    welcomeEmbed.set_footer(text=f"{len(member.guild.members)}.Üye",icon_url="attachment://evos.png")                  
                    
                    await channel.send(file=file,embed=welcomeEmbed)         
        except Exception as error:
            logger.info(f"Guild | Data | Error : {error}")
            pass

    @commands.Cog.listener()
    async def on_member_remove(self,member):       
        if member.name != self.client.user.name :
            
            try :
                jsonFile = open(dataSource, "r")
                ServerData = json.load(jsonFile)
                jsonFile.close()
                channelID = ServerData[str(member.guild.id)]['LEAVE_CHANNEL_ID']
                channel = discord.utils.get(member.guild.text_channels, id=int(channelID))
                
                if channel != None :
                    leaveEmbed = discord.Embed(title = "Aramızdan birisi eksildi !",description = f"{member.mention} Aramızdan ayrıldı !",colour=0xd8f500)
                    leaveEmbed.set_author(name=member.guild.name,icon_url=member.guild.icon_url)
                    leaveEmbed.set_thumbnail(url=member.avatar_url)
                    file = discord.File("images/evos.png", filename="evos.png")
                    leaveEmbed.set_footer(text=f"{len(member.guild.members)} Üye",icon_url="attachment://evos.png")      
                    
                    await channel.send(file=file,embed=leaveEmbed)
                else :
                    pass
            except :
                pass
  
    @commands.Cog.listener()
    async def on_guild_join(self, guild):
        try :
            jsonFile = open(dataSource, "r")
            data = json.load(jsonFile)
            jsonFile.close()
            data[str(guild.id)] = {}
            data[str(guild.id)]["CUSTOM_PREFIX"] = "."          
            
            with open (dataSource, 'w+') as f:
                json.dump(data, f,indent=4)
            
            try :
                infoEmbed = discord.Embed(title = "Evos'u sunucuna eklediğin için teşekkürler!",colour=0xd8f500)
                infoEmbed.add_field(name="Prefix(Özelleştirilebilir)",value="Varsayılan: **.**(Nokta)",inline=False)
                infoEmbed.add_field(name="Komut Listesi",value="Komutları görmek için **.yardım** yazabirsin.",inline=False)
                infoEmbed.add_field(name="Geliştirici misin ?",value="[Buradan](https://github.com/semihaydin0/Evos) kaynak kodlarını inceleyebilirsin.",inline=False)
                file = discord.File("images/evos.png", filename="evos.png")
                infoEmbed.set_thumbnail(url="attachment://evos.png")          
                
                await guild.text_channels[0].send(file=file,embed=infoEmbed)
            except :
                pass
        except Exception as error:
            logger.info(f"Guild | OnGuildJoin | Error : {error}")
            pass

def setup(client):
    client.add_cog(Guild(client))