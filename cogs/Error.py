#MIT License
#Copyright (c) 2020 Semih Aydın
#UTF-8

import discord
from discord.ext import commands
from logging_files.error_log import logger

class Error(commands.Cog):
    def __init__(self,client):
        self.client = client
    
    @commands.Cog.listener()
    async def on_command_error(self,ctx,error):
        if isinstance(error , commands.CommandNotFound):
            """CommandNotFound"""
            pass

            logger.info(f"Error | CommandNotFound : {ctx.message.content} | Tarafından : {ctx.author}")

        if isinstance(error , commands.MissingRequiredArgument):
            """MissingRequiredArgument"""
            commandErrorEmbed = discord.Embed(title="Eksik Argüman Girişi",description="Gerekli argümanlara **.help** komutu ile ulaşabilirsin.",colour = 0xffd500)
            
            await ctx.send(embed = commandErrorEmbed)

            logger.info(f"Error | Komut : {ctx.message.content} | MissingRequiredArgument : {ctx.author}")

        if isinstance(error , commands.MissingPermissions):
            """MissingPermissions"""
            commandErrorEmbed_2 = discord.Embed(title="Yetersiz Yetki",description="Diğer komutlara **.yardım** komutu ile ulaşabilirsin.",colour = 0xffd500)
            
            await ctx.send(embed = commandErrorEmbed_2)

            logger.info(f"Error | Komut : {ctx.message.content} | MissingPermissions : {ctx.author}")

        if isinstance(error, commands.BotMissingPermissions):
            """BotMissingPermissions"""
            commandErrorEmbed_3 = discord.Embed(title="Yetersiz Yetki",description=f"{self.client.user.name} bu komutu gerekli izinlere sahip olmadan uygulayamaz.",colour = 0xffd500)
            
            await ctx.send(embed = commandErrorEmbed_3)

            logger.info(f"Error | Komut : {ctx.message.content} | BotMissingPermissions : {ctx.guild.name}")

def setup(client):
    client.add_cog(Error(client))