#MIT License
#Copyright (c) 2020 Semih Aydın
#UTF-8

import discord
from discord.ext import commands
import os
import sys
import wget
import subprocess
from logging_files.admin_log import logger

class Admin(commands.Cog):
    def __init__(self,client):
        self.client = client

    @commands.is_owner()
    @commands.command(name = "Load",aliases=['load'],hidden=True)
    async def load_command(self,ctx,module :str):
        moduleStatus = False

        for filename in os.listdir('./cogs'):
            if filename.endswith('.py'):
                if module == filename[:-3] :

                    try :
                        self.client.load_extension(f'cogs.{filename[:-3]}')
                        loadEmbed=discord.Embed(title=f"{filename[:-3]} adlı modül yüklendi.",colour=0xffd500)
                        await ctx.send(embed=loadEmbed)

                        logger.info(f"Admin | Load | Tarafından : {ctx.author}")
                    except Exception as e:
                        loadEmbed_2=discord.Embed(title=f"{filename[:-3]} adlı modül yüklenemedi.",description ="Modül halihazırda yüklenmiş olabilir.",colour=0xffd500)
                        await ctx.send(embed=loadEmbed_2)

                        logger.error(f"Admin | Load | Filename: {filename[:-3]} | Error: {e}")

                    moduleStatus=True

        if moduleStatus == False :
            loadEmbed_3=discord.Embed(title=f"{module} adlı modül bulunamadı.",colour=0xffd500)

            await ctx.send(embed=loadEmbed_3)

    @commands.is_owner()
    @commands.command(name="Unload",aliases=['unload'],hidden=True)
    async def unload_command(self,ctx,module: str):
        moduleStatus = False

        for filename in os.listdir('./cogs'):
            if filename.endswith('.py'):
                if module == filename[:-3] :

                    try :
                        self.client.unload_extension(f'cogs.{filename[:-3]}')
                        unloadEmbed=discord.Embed(title=f"{filename[:-3]} adlı modül kaldırıldı.",colour=0xffd500)
                        await ctx.send(embed=unloadEmbed)

                        logger.info(f"Admin | Unload | Tarafından : {ctx.author}")
                    except Exception as e:
                        unloadEmbed_2=discord.Embed(title=f"{filename[:-3]} adlı modül kaldırılamadı.",description ="Modül halihazırda kaldırılmış olabilir.",colour=0xffd500)
                        await ctx.send(embed=unloadEmbed_2)

                        logger.error(f"Admin | Unload | Filename: {filename[:-3]} | Error: {e}")

                    moduleStatus = True

        if moduleStatus == False :
            unloadEmbed_3=discord.Embed(title=f"{module} adlı modül bulunamadı.",colour=0xffd500)

            await ctx.send(embed=unloadEmbed_3)

    @commands.is_owner()
    @commands.command(name="Reload",aliases=['reload'],hidden=True)
    async def reload_command(self,ctx,module: str):
        moduleStatus = False

        for filename in os.listdir('./cogs'):
            if filename.endswith('.py'):
                if module == filename[:-3] :

                    try :
                        self.client.reload_extension(f'cogs.{filename[:-3]}')
                        reloadEmbed=discord.Embed(title=f"{filename[:-3]} adlı modül yeniden yüklendi.",colour=0xffd500)
                        await ctx.send(embed=reloadEmbed)

                        logger.info(f"Admin | Reload | Tarafından: {ctx.author}")
                    except Exception as e:
                        reloadEmbed_2=discord.Embed(title=f"{filename[:-3]} adlı modül yeniden yüklenemedi.",colour=0xffd500)
                        await ctx.send(embed=reloadEmbed_2)

                        logger.error(f"Admin | Reload | Filename: {filename[:-3]} | Error: {e}")

                    moduleStatus = True

        if moduleStatus==False :
            reloadEmbed_3=discord.Embed(title=f"{module} adlı modül bulunamadı.",colour=0xffd500)

            await ctx.send(embed=reloadEmbed_3)

    @commands.is_owner()
    @commands.command(name="ReloadAll",aliases=['reloadall'],hidden=True)
    async def reload_all_command(self,ctx):
        reloadEmbed=discord.Embed(title="Tüm Modülleri Yeniden Yükle",colour=0xffd500)
        for filename in os.listdir('./cogs'):
            if filename.endswith('.py'):

                    try :
                        self.client.reload_extension(f'cogs.{filename[:-3]}')
                        reloadEmbed.add_field(name=f"{filename[:-3]}",value="İşlem Durumu: `BAŞARILI`")
                    except Exception as e:
                        reloadEmbed.add_field(name=f"{filename[:-3]}",value="İşlem Durumu: `BAŞARISIZ`")

                        logger.error(f"Admin | Reload | Filename: {filename[:-3]} | Error: {e}")

        await ctx.send(embed = reloadEmbed)

        logger.info(f"Admin | ReloadAll | Tarafından: {ctx.author}")

    @commands.is_owner()
    @commands.command(name="Log",aliases=['log'],hidden=True)
    async def send_log_command(self, ctx,name: str):
        logStatus = False

        for filename in os.listdir('./logs'):
            if filename.endswith('.log'):
                if name+".log" == filename:
                    logFile = discord.File(f"./logs/{name}.log",filename=f"{name}.log")

                    await ctx.author.send(file=logFile)
                    logEmbed=discord.Embed(title=f"{name} adlı log DM üzerinden gönderildi.",colour=0xffd500)

                    await ctx.send(embed=logEmbed)
                    logStatus=True

                    logger.info(f"Admin | Log: {name} | Tarafından: {ctx.author}")

        if logStatus==False :
            logEmbed_2=discord.Embed(title=f"{name} adlı log bulunamadı.",colour=0xffd500)

            await ctx.send(embed=logEmbed_2)

    @commands.is_owner()
    @commands.command(name="ChangeUsername",aliases=['changeusername'],hidden=True)
    async def change_username_command(self, ctx, *, name: str):
        try:
            await self.client.user.edit(username=name)
            changeUsernameEmbed=discord.Embed(title="Kullanıcı adı değişikliği başarılı.",colour=0xffd500)

            await ctx.send(embed = changeUsernameEmbed)

            logger.info(f"Admin | ChangeUsername | Tarafından: {ctx.author}")
        except Exception as e:
            changeUsernameEmbed_2=discord.Embed(title="Hata",description =f"{e}",colour=0xffd500)
            await ctx.send(embed = changeUsernameEmbed_2)

            logger.error(f"Admin | ChangeUsername | Error: {e}")

    @commands.is_owner()
    @commands.command(name="ChangeAvatar",aliases=['changeavatar'],hidden=True)
    async def change_avatar_command(self, ctx, url: str):
        try:
            avatar_filename = wget.download(url)
            fp = open(avatar_filename, 'rb')
            pfp = fp.read()
            await self.client.user.edit(avatar=pfp)

            changeAvatarEmbed=discord.Embed(title="Avatar değişikliği başarılı.",colour=0xffd500)

            await ctx.send(embed = changeAvatarEmbed)
            os.remove(avatar_filename)

            logger.info(f"Admin | ChangeAvatar | Tarafından: {ctx.author}")
        except Exception as e:
            changeAvatarEmbed_2=discord.Embed(title="Hata",description =f"{e}",colour=0xffd500)
            await ctx.send(embed = changeAvatarEmbed_2)
            os.remove(avatar_filename)

            logger.error(f"Admin | ChangeAvatar | Error: {e}")

    @commands.is_owner()
    @commands.command(name="LeaveServer",aliases=['leaveserver'],hidden=True)
    async def leave_server_command(self, ctx, serverID: str):
        try:
            if serverID == '1' :
                await ctx.guild.leave()
            else:
                guild = self.client.get_guild(int(serverID))
                if guild:
                    await guild.leave()

                    leaveServerEmbed=discord.Embed(title=f"{guild.name} adlı sunucudan ayrılma başarılı.",colour=0xffd500)

                    await ctx.send(embed = leaveServerEmbed)
                else :
                    leaveServerEmbed_2=discord.Embed(title=f"{self.client.user.name} bu ID'ye sahip bir sunucuda bulunmuyor.",colour=0xffd500)

                    await ctx.send(embed = leaveServerEmbed_2)
            logger.info(f"Admin | LeaveServer | Tarafından: {ctx.author}")
        except Exception as e:
            leaveServerEmbed_3=discord.Embed(title="Hata",description =f"{e}",colour=0xffd500)
            await ctx.send(embed = leaveServerEmbed_3)

            logger.error(f"Admin | LeaveServer | Error: {e}")

    @commands.is_owner()
    @commands.command(name="Activity",aliases=['activity'],hidden=True)
    async def activity_command(self, ctx, acType: str, *, acName: str):
        acType = acType.lower()
        if acType == 'playing':
            type_ = discord.ActivityType.playing
        elif acType == 'watching':
            type_ = discord.ActivityType.watching
        elif acType == 'listening':
            type_ = discord.ActivityType.listening

        try:
            if acType == 'streaming' :
                await self.client.change_presence(activity=discord.Streaming(name='Canlı', url=acName))
            else :
                await self.client.change_presence(activity=discord.Activity(type=type_, name=acName))
            activityEmbed=discord.Embed(title="Aktivite değişikliği başarılı.",colour=0xffd500)

            await ctx.send(embed=activityEmbed)

            logger.info(f"Admin | Activity: {acName}({acType}) | Tarafından: {ctx.author}")
        except Exception as e:
            activityEmbed_2=discord.Embed(title="Hata",description =f"{e}",colour=0xffd500)
            await ctx.send(embed = activityEmbed_2)

            logger.error(f"Admin | Activity | Error: {e}")

    @commands.is_owner()
    @commands.command(name="Restart",aliases=['restart'],hidden=True)
    async def restart_command(self,ctx):
        restartEmbed=discord.Embed(title=f"{self.client.user.name} yeniden başlatılıyor.",colour=0xffd500)

        message = await ctx.send(embed = restartEmbed)
        try :
            await self.client.logout()
            subprocess.call([sys.executable, "Evos.py"])

            logger.info(f"Admin | Restart | Tarafından: {ctx.author}")
        except Exception as e:
            restartEmbed_2=discord.Embed(title=f"{self.client.user.name} yeniden başlatılırken bir hata meydana geldi.",colour=0xffd500)
            await message.edit(embed = restartEmbed_2)

            logger.error(f"Admin | Restart | Error: {e}")

    @commands.is_owner()
    @commands.command(name="Off",aliases=['off'],hidden=True)
    async def off_command(self, ctx):
        offEmbed=discord.Embed(title=f"{self.client.user.name} kapatılıyor.",colour=0xffd500)

        message = await ctx.send(embed=offEmbed)
        try:
            await self.client.logout()
        except Exception as e:
            offEmbed_2=discord.Embed(title="Hata",description =f"{e}",colour=0xffd500)
            await message.edit(embed = offEmbed_2)

            logger.error(f"Admin | Off | Error: {e}")

def setup(client):
    client.add_cog(Admin(client))