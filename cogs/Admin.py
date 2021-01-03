#MIT License
#Copyright (c) 2020 Semih Aydın
#UTF-8

import os
import discord
from discord.ext import commands

from logging_files.admin_log import logger

class Admin(commands.Cog):
    def __init__(self,client):
        self.client = client

    @commands.is_owner()
    @commands.command(name = "load",aliases=['yükle'],hidden=True)
    async def load_command(self,ctx,module :str):
        """Loads Module
        Use of : load {module_name}
        """
        status = False

        for filename in os.listdir('./cogs'):
            if filename.endswith('.py'):
                if module == filename[:-3] :
                    try :
                        self.client.load_extension(f'cogs.{filename[:-3]}')
                        load_embed=discord.Embed(title=f"{filename[:-3]} adlı modül yüklendi.",colour=0xffd500)
                        await ctx.send(embed=load_embed)
                        status=True

                        logger.info(f"Admin | Modül Yükleme | Tarafından : {ctx.author}")
                    except :
                        loader_embed=discord.Embed(title=f"{filename[:-3]} adlı modül yüklenemedi.",description ="Modül halihazırda yüklenmiş olabilir.",colour=0xffd500)
                        await ctx.send(embed=loader_embed)
                        status=True

        if status==False :
            loader2_embed=discord.Embed(title=f"{module} adlı modül bulunamadı.",colour=0xffd500)
            await ctx.send(embed=loader2_embed)

    @commands.is_owner()
    @commands.command(name="unload",aliases=['kaldır'],hidden=True)
    async def unload_command(self,ctx,module :str):
        """Unloads Module
        Use of : unload {module_name}
        """
        status = False

        for filename in os.listdir('./cogs'):
            if filename.endswith('.py'):
                if module == filename[:-3] :
                    try :
                        self.client.unload_extension(f'cogs.{filename[:-3]}')
                        unload_embed=discord.Embed(title=f"{filename[:-3]} adlı modül kaldırıldı.",colour=0xffd500)
                        await ctx.send(embed=unload_embed)
                        status=True

                        logger.info(f"Admin | Modül Kaldırma | Tarafından : {ctx.author}")
                    except :
                        unloader_embed=discord.Embed(title=f"{filename[:-3]} adlı modül kaldırılamadı.",description ="Modül halihazırda kaldırılmış olabilir.",colour=0xffd500)
                        await ctx.send(embed=unloader_embed)
                        status=True

        if status==False :
            loader2_embed=discord.Embed(title=f"{module} adlı modül bulunamadı.",colour=0xffd500)
            await ctx.send(embed=loader2_embed)

    @commands.is_owner()
    @commands.command(name="reload",aliases=['tekraryükle'],hidden=True)
    async def reload_command(self,ctx,module :str):
        """Reloads Module
        Use of : reload {module_name}
        """
        status = False

        for filename in os.listdir('./cogs'):
            if filename.endswith('.py'):
                if module == filename[:-3] :
                    try :
                        self.client.unload_extension(f'cogs.{filename[:-3]}')
                        self.client.load_extension(f'cogs.{filename[:-3]}')
                        reload_embed=discord.Embed(title=f"{filename[:-3]} adlı modül yeniden yüklendi.",colour=0xffd500)
                        await ctx.send(embed=reload_embed)
                        status=True

                        logger.info(f"Admin | Yeniden Modül Yükleme | Tarafından : {ctx.author}")
                    except :
                        reloader_embed=discord.Embed(title=f"{filename[:-3]} adlı modül yeniden yüklenemedi.",colour=0xffd500)
                        await ctx.send(embed=reloader_embed)
                        status=True

        if status==False :
            loader2_embed=discord.Embed(title=f"{module} adlı modül bulunamadı.",colour=0xffd500)
            await ctx.send(embed=loader2_embed)                

    @commands.is_owner()
    @commands.command(name="log",aliases=['günlük'],hidden=True)
    async def log_command(self, ctx,name):
        """Send The Logs
        Use of : log {log_name}
        """
        status = False

        for filename in os.listdir('./logs'):
            if filename.endswith('.log'):
                if name+".log" == filename:
                    logfile = discord.File(f"./logs/{name}.log",filename=f"{name}.log")
                    await ctx.author.send(file=logfile)
                    log_embed=discord.Embed(title=f"{name} adlı günlük kaydı DM üzerinden gönderildi.",colour=0xffd500)
                    await ctx.send(embed=log_embed)
                    status=True

                    logger.info(f"Admin | Günlük Kaydı : {name} | Tarafından : {ctx.author}")

        if status==False :
            loger_embed=discord.Embed(title=f"{name} adlı günlük kaydı bulunamadı.",colour=0xffd500)
            await ctx.send(embed=loger_embed)

    @commands.is_owner()
    @commands.command(name="activity",aliases=['aktivite'],hidden=True)
    async def activity_command(self, ctx,name):
        """Changing Activity
        Use of : activity {name}
        """
        activity = ".yardım | "

        if name == "default" :
            activity+="🎵 HIGH QUALITY MUSIC"
        else :
            name = name.replace("."," ")
            activity += name

        await self.client.change_presence(status=discord.Status.online , activity=discord.Game(f"{activity}"))           
        activity_embed=discord.Embed(title="Aktivite değişikliği başarılı.",colour=0xffd500)
        await ctx.send(embed=activity_embed)

        logger.info(f"Admin | Aktivite Değişikliği : {name} | Tarafından : {ctx.author}")

    @commands.is_owner()
    @commands.command(name="off",aliases=['kapat'],hidden=True)
    async def off_command(self, ctx):
        """End The Bot Session
        Use of : off
        """
        off_embed=discord.Embed(title=f"{self.client.user.name} kapatılıyor.",colour=0xffd500)
        await ctx.send(embed=off_embed)

        logger.info(f"Admin | Kapatma Talebi | Tarafından : {ctx.author}")

        await self.client.logout()

def setup(client):
    client.add_cog(Admin(client))