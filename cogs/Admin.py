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
    @commands.command(name = "Load",aliases=['load'],hidden=True)
    async def load_command(self,ctx,module :str):
        """Loads Module
        Use of : load {module}
        """
        moduleStatus = False
        
        for filename in os.listdir('./cogs'):
            if filename.endswith('.py'):
                if module == filename[:-3] :
                    
                    try :
                        self.client.load_extension(f'cogs.{filename[:-3]}')
                        loadEmbed=discord.Embed(title=f"{filename[:-3]} adlı modül yüklendi.",colour=0xffd500)
                        await ctx.send(embed=loadEmbed)
                        
                        logger.info(f"Admin | Load | Tarafından : {ctx.author}")
                    except :
                        loadEmbed_2=discord.Embed(title=f"{filename[:-3]} adlı modül yüklenemedi.",description ="Modül halihazırda yüklenmiş olabilir.",colour=0xffd500)
                        
                        await ctx.send(embed=loadEmbed_2)
                    
                    modulestatus=True    
        
        if moduleStatus == False :
            loadEmbed_3=discord.Embed(title=f"{module} adlı modül bulunamadı.",colour=0xffd500)
            
            await ctx.send(embed=loadEmbed_3)

    @commands.is_owner()
    @commands.command(name="Unload",aliases=['unload'],hidden=True)
    async def unload_command(self,ctx,module :str):
        """Unloads Module
        Use of : unload {module}
        """
        modulestatus = False
        
        for filename in os.listdir('./cogs'):
            if filename.endswith('.py'):
                if module == filename[:-3] :
                    
                    try :
                        self.client.unload_extension(f'cogs.{filename[:-3]}')
                        unloadEmbed=discord.Embed(title=f"{filename[:-3]} adlı modül kaldırıldı.",colour=0xffd500)
                        await ctx.send(embed=unloadEmbed)
                        
                        logger.info(f"Admin | Unload | Tarafından : {ctx.author}")
                    except :
                        unloadEmbed_2=discord.Embed(title=f"{filename[:-3]} adlı modül kaldırılamadı.",description ="Modül halihazırda kaldırılmış olabilir.",colour=0xffd500)
                        
                        await ctx.send(embed=unloadEmbed_2)
                    
                    modulestatus = True
        
        if modulestatus == False :
            unloadEmbed_3=discord.Embed(title=f"{module} adlı modül bulunamadı.",colour=0xffd500)
            
            await ctx.send(embed=unloadEmbed_3)

    @commands.is_owner()
    @commands.command(name="Reload",aliases=['reload'],hidden=True)
    async def reload_command(self,ctx,module : str):
        """Reloads Module
        Use of : reload {module}
        """
        modulestatus = False
        
        for filename in os.listdir('./cogs'):
            if filename.endswith('.py'):
                if module == filename[:-3] :
                    
                    try :
                        self.client.unload_extension(f'cogs.{filename[:-3]}')
                        self.client.load_extension(f'cogs.{filename[:-3]}')
                        reloadEmbed=discord.Embed(title=f"{filename[:-3]} adlı modül yeniden yüklendi.",colour=0xffd500)
                        await ctx.send(embed=reloadEmbed)
                        
                        logger.info(f"Admin | Reload | Tarafından : {ctx.author}")
                    except :
                        reloadEmbed_2=discord.Embed(title=f"{filename[:-3]} adlı modül yeniden yüklenemedi.",colour=0xffd500)
                        
                        await ctx.send(embed=reloadEmbed_2)
                    
                    modulestatus = True
        if modulestatus==False :
            reloadEmbed_3=discord.Embed(title=f"{module} adlı modül bulunamadı.",colour=0xffd500)
            
            await ctx.send(embed=reloadEmbed_3)

    @commands.is_owner()
    @commands.command(name="Log",aliases=['log'],hidden=True)
    async def log_command(self, ctx,name : str):
        """Send The Logs
        Use of : log {name}
        """
        logStatus = False
        
        for filename in os.listdir('./logs'):
            if filename.endswith('.log'):
                if name+".log" == filename:
                    logFile = discord.File(f"./logs/{name}.log",filename=f"{name}.log")
                    
                    await ctx.author.send(file=logFile)
                    logEmbed=discord.Embed(title=f"{name} adlı log DM üzerinden gönderildi.",colour=0xffd500)
                    
                    await ctx.send(embed=logEmbed)
                    logStatus=True
                    
                    logger.info(f"Admin | Log : {name} | Tarafından : {ctx.author}")
        
        if logStatus==False :
            logEmbed_2=discord.Embed(title=f"{name} adlı log bulunamadı.",colour=0xffd500)
            
            await ctx.send(embed=logEmbed_2)

    @commands.is_owner()
    @commands.command(name="Activity",aliases=['activity'],hidden=True)
    async def activity_command(self, ctx,name : str):
        """Changing Activity
        Use of : activity {name}
        """
        name = name.replace("."," ")
        
        await self.client.change_presence(status=discord.Status.online , 
            activity=discord.Game(name))
        activityEmbed=discord.Embed(title="Aktivite değişikliği başarılı.",colour=0xffd500)
        
        await ctx.send(embed=activityEmbed)
        
        logger.info(f"Admin | Activity : {name} | Tarafından : {ctx.author}")

    @commands.is_owner()
    @commands.command(name="off",aliases=['kapat'],hidden=True)
    async def off_command(self, ctx):
        """End The Bot Session
        Use of : off
        """
        offEmbed=discord.Embed(title=f"{self.client.user.name} kapatılıyor.",colour=0xffd500)
        
        await ctx.send(embed=offEmbed)
        logger.info(f"Admin | Off | Tarafından : {ctx.author}")
        
        await self.client.logout()

def setup(client):
    client.add_cog(Admin(client))