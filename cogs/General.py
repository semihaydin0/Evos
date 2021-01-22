#MIT License
#Copyright (c) 2020 Semih Aydın
#UTF-8

import discord
from discord.ext import commands
from cpuinfo import get_cpu_info
from uptime import uptime
import platform
import psutil
import math
from logging_files.general_log import logger

def get_size(bytes, suffix="B"):
    factor = 1024
    for unit in ["", "K", "M", "G", "T", "P"]:
        if bytes < factor:
            return f"{bytes:.2f}{unit}{suffix}"
        bytes /= factor

class General(commands.Cog):
    def __init__(self,client):
        self.client = client

    @commands.command(name ="Ping",brief ="Evos'un gecikme değerini gösterir.",aliases = ['ping','Latency','latency'])
    async def ping_command(self,ctx):
        """Ping
        Use of : ping
        """
        pingEmbed = discord.Embed(title = f'Ping: {round(self.client.latency * 1000)} ms',color=0xd8f500)
        pingEmbed.set_footer(text=f"Tarafından: {ctx.author}",icon_url=ctx.author.avatar_url)

        await ctx.send(embed=pingEmbed)

        logger.info(f"General | Ping | Tarafından: {ctx.author}")

    @commands.guild_only()
    @commands.command(name ="Davet",brief ="Kanal davet linki oluşturur.",aliases=['davet','Invite','invite'])
    async def invite_command(self,ctx,time: int = 0,amount: int = 0):
        """Invite
        Use of : invite
        """
        link = await ctx.channel.create_invite(max_age = time*3600,max_uses = amount)
        
        if time == 0:
            time = "Süresiz"
        
        if amount == 0:
            amount = "Limitsiz"
        inviteEmbed=discord.Embed(
            description =f"Davet Linki: {link}\nBu davetin geçerlilik süresi: {time} saat\nBu davetin maksimum kullanım sayısı: {amount}",color=0xd8f500,timestamp=ctx.message.created_at)
        inviteEmbed.set_author(name=ctx.message.guild.name,icon_url=ctx.message.guild.icon_url)
        inviteEmbed.set_footer(text=f"Tarafından: {ctx.author}",icon_url=ctx.author.avatar_url)

        await ctx.send(embed=inviteEmbed)

        logger.info(f"General | Invite | Tarafından: {ctx.author}")

    @commands.command(name ="Evos",brief ="Evos'un davet linkini gönderir.",aliases=["evos"])
    async def evos_invite_command(self,ctx):
        """Evos
        Use of : evos
        """
        evosEmbed=discord.Embed(title =f"Evos - Türkçe Discord Botu",description ="**Bu [linkten](https://discord.com/api/oauth2/authorize?client_id=675459603420545056&permissions=8&scope=bot)** beni sunucuna ekleyebilirsin.",color=0xd8f500,timestamp=ctx.message.created_at)
        evosEmbed.add_field(name="Geliştirici misin ?",value="[Buradan](https://github.com/semihaydin0/Evos) kaynak kodlarını inceleyebilirsin.",inline=False)

        file = discord.File("images/evos.png", filename="evos.png")
        evosEmbed.set_footer(text=f"Teşekkürler!",icon_url="attachment://evos.png")

        await ctx.send(file=file,embed=evosEmbed)

        logger.info(f"General | Evos | Tarafından: {ctx.author}")

    @commands.command(name="Hesapla",brief="İki sayı ile dört işlem yapar.",aliases = ['hesapla','Math','math'])
    async def math_command(self,ctx,num1: float,op: str,num2: float):
        """Math
        Use of : math {number1} {operator} {number2}
        """
        result = 0.0
        
        if op == "+":
            result = num1 + num2

        elif op == "-":
            result = num1 - num2

        elif op == "*":
            result = num1 * num2

        elif op == "/":
            result = num1 / num2

        else :
            mathEmbed_2 = discord.Embed(title="Hata",description="Hatalı operatör girişi.**(+,-,*,/)**",color=0xd8f500) 
            await ctx.send(embed=mathEmbed_2)
            return
        
        mathEmbed = discord.Embed(title="Sonuç",description=f"{num1}{op}{num2} işleminin sonucu = **{result}**",color=0xd8f500)
        mathEmbed.set_footer(text=f"Tarafından: {ctx.author}",icon_url=ctx.author.avatar_url)
        
        await ctx.send(embed=mathEmbed)

        logger.info(f"General | Math | Tarafından: {ctx.author}")

    @commands.command(name ="Yardım",brief ="Komutlar hakkında bilgi verir.",aliases=["yardım"])
    async def help_command(self,ctx,cog="1"):
        """Help
        Use of : yardım
        """
        helpEmbed=discord.Embed(title="🤖 Komutlar",description="Komutların kullanımlarını görmek için **.help** yazabilirsin.", color=0xd8f500,timestamp=ctx.message.created_at)
        file = discord.File("images/evos.png", filename="evos.png")
        helpEmbed.set_thumbnail(url="attachment://evos.png")
        
        cogs = [c for c in self.client.cogs.keys()]
        cogs.remove('Admin')
        cogs.remove('Error')
        cogs.remove('Events')
        totalPages = math.ceil(len(cogs) / 4)
        
        cog = int(cog)
            
        if cog > totalPages or cog < 1:
            helpEmbed_2 = discord.Embed(title="Hata",description="Hatalı sayfa numarası.",colour=0xd8f500)
                
            await ctx.send(embed=helpEmbed_2)
            return
        helpEmbed.set_footer(text=f"{cog}.Sayfa | Toplam Sayfa: {totalPages} | PHOENIX#7103 tarafından 💖 ile geliştirildi!")
        neededCogs = []
            
        for i in range(4):
            x = i + (int(cog) - 1) * 4
            try:
                neededCogs.append(cogs[x])
            except IndexError:
                pass
            
        for cog in neededCogs:
            commandList = ""
                
            for command in self.client.get_cog(cog).walk_commands():
                if command.hidden:
                    continue
                elif command.parent != None:
                    continue
                commandList += f"**{command.name}** - *{command.brief}*\n"
            commandList += "\n"
            helpEmbed.add_field(name=cog, value=commandList, inline=False)
        
        await ctx.send(file=file,embed=helpEmbed)
        
        logger.info(f"General | Help | Tarafından: {ctx.author}")

    @commands.command(name="Evosinfo",brief="Evos'un istatistiklerini gösterir.",aliases=["evosinfo"])
    async def info_command(self,ctx):
        """Stats
        Use of : stats
        """
        svmem = psutil.virtual_memory()
        day = int(uptime()/3600/24)
        hours = int(uptime()/3600-day*24)
        minute = int(uptime()/60)-day*24*60-hours*60
        second = int(uptime())-day*24*3600-hours*3600-minute*60
        statsEmbed=discord.Embed(title=f"📃 {self.client.user.name} Hakkında",color=0xd8f500,timestamp=ctx.message.created_at)
        statsEmbed.add_field(
            name="Teknik Bilgiler",value=f"Python Versiyonu: **{platform.python_version()}**\nDiscord.py Versiyonu: **{discord.__version__}**\nÇalışma Zamanı: **{day} Gün, {hours} Saat, {minute} Dakika, {second} Saniye**\nCPU(İşlemci): **{get_cpu_info()['brand_raw']}**\nFiziksel Çekirdekler: **{psutil.cpu_count(logical=False)}**\nToplam Çekirdek: **{psutil.cpu_count(logical=True)}**\nOS(İşletim Sistemi): **{platform.platform()}**\nKullanılan Bellek: **{get_size(svmem.used)}**\nKullanılabilir Bellek: **{get_size(svmem.available)}**\nToplam Bellek: **{get_size(svmem.total)}**\nKullanımdaki Bellek Yüzdesi: **%{svmem.percent}**\nBarındırılan Sunucu: **Google Cloud - EU WEST**")
        statsEmbed.set_footer(text="PHOENIX#7103 tarafından 💖 ile geliştirildi!",icon_url=ctx.author.avatar_url)
        
        file = discord.File("images/evos.png", filename="evos.png")
        statsEmbed.set_thumbnail(url="attachment://evos.png")

        await ctx.send(file=file,embed=statsEmbed)

        logger.info(f"General | Evosinfo | Tarafından: {ctx.author}")

def setup(client):
    client.add_cog(General(client))