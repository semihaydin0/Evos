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

            logger.info(f"Error | Komut Bulunamadı : {ctx.message.content} | Tarafından : {ctx.author}")

        if isinstance(error , commands.MissingRequiredArgument):
            """MissingRequiredArgument"""
            await ctx.send(f"{ctx.author.mention} Eksik argüman girişi. **.help <komut>** yazıp komut için gerekli olan argümana ulaşabilirsin.")

            logger.info(f"Error | Komut : {ctx.message.content} | Eksik Argüman Tespiti : {ctx.author}")

        if isinstance(error , commands.MissingPermissions):
            """MissingPermissions"""
            await ctx.send(f"{ctx.author.mention} Bu komut için yeterli yetkiye sahip değilsin. **.yardım** yazarak diğer komutlara göz atabilirsin.")

            logger.info(f"Error | Komut : {ctx.message.content} | Eksik Yetki : {ctx.author}")

        if isinstance(error, commands.BotMissingPermissions):
            """BotMissingPermissions"""
            await ctx.send(f"{ctx.author.mention} Bu komut için Evos'un **yönetici** rolüne ihtiyacı var. Roller kısmından Evos rolüne yönetici izni vermeni öneriyoruz.")

            logger.info(f"Error | Komut : {ctx.message.content} | Evos yeterli yetkiye sahip değil : {ctx.guild.name}")

def setup(client):
    client.add_cog(Error(client))