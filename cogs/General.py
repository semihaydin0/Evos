#MIT License
#Copyright (c) 2020 Semih Aydın
#UTF-8

import discord
from discord.utils import get
from discord.ext import commands
import platform
from cpuinfo import get_cpu_info
from uptime import uptime
import psutil

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

    @commands.command(name = "Ping",brief = "Evos'un gecikme değerini gösterir.",aliases = ["latency","ping"])
    async def ping_command(self,ctx):
        """Ping
        Use of : ping
        """
        client_latency =  round(self.client.latency * 1000)

        PingEmbed = discord.Embed(title = f'Ping : {client_latency} ms',color=0xd8f500)
        PingEmbed.set_footer(text=f"İstek Sahibi : {ctx.author.name}",icon_url=ctx.author.avatar_url)

        await ctx.send(embed=PingEmbed)

        logger.info(f"General | Ping : {client_latency} ms  | Tarafından : {ctx.author}")

    @commands.guild_only()
    @commands.command(name = "Davet",brief = "Sunucu davet linki oluşturur.",aliases=["invite","davet"])
    async def guild_invite_command(self,ctx):
        """Invite
        Use of : invite
        """
        link = await ctx.channel.create_invite(max_age = 300)

        GuildInvt=discord.Embed(description =f"**Davet Linki** : {link}" ,color=0xd8f500)
        GuildInvt.set_author(name=ctx.message.guild.name,icon_url=ctx.message.guild.icon_url)
        GuildInvt.set_footer(text=f"İstek Sahibi : {ctx.author.name}",icon_url=ctx.author.avatar_url)

        await ctx.send(embed=GuildInvt)

        logger.info(f"General | Sunucu Daveti : {ctx.guild.name} | Tarafından : {ctx.author}")

    @commands.command(name = "Evos",brief = "Evos'un davet linkini gönderir.",aliases=["evos"])
    async def evos_invite_command(self,ctx):
        """Evos
        Use of : evos
        """
        evosinviteEmbed=discord.Embed(title =f"Evos - Türkçe Discord Botu",description ="**Bu [linke](https://discord.com/api/oauth2/authorize?client_id=675459603420545056&permissions=8&scope=bot)** tıklayarak beni sunucuna ekleyebilirsin." ,color=0xd8f500,timestamp=ctx.message.created_at)
        evosinviteEmbed.add_field(name="Kaynak Kodları",value="https://github.com/semihaydin0/Evos")

        file = discord.File("images/evos.png", filename="evos.png")
        evosinviteEmbed.set_footer(text=f"Teşekkürler !",icon_url="attachment://evos.png")

        await ctx.send(file=file,embed=evosinviteEmbed)

        logger.info(f"General | Bot Daveti | Tarafından : {ctx.author}")

    @commands.command(name="Hesapla",brief= "İki sayı ile dört işlem yapar.",aliases = ['hesapla','math'])
    async def math_command(self,ctx,num1 : int ,op,num2: int):
        """Math
        Use of : math {number1} {operator} {number2}
        """
        result = 0.0

        if op == "+":
            result = num1 + num2
            await ctx.send(f"{num1}{op}{num2} işleminin sonucu = **{result}**")

        elif op == "-":
            result = num1 - num2
            await ctx.send(f"{num1}{op}{num2} işleminin sonucu = **{result}**")

        elif op == "*":
            result = num1 * num2
            await ctx.send(f"{num1}{op}{num2} işleminin sonucu = **{result}**")

        elif op == "/":
            result = num1 / num2
            await ctx.send(f"{num1}{op}{num2} işleminin sonucu = **{result}**")

        else : 
            await ctx.send(f"**Hatalı operatör girişi.(Sadece + - * /)**")

        logger.info(f"General | Hesapla | Tarafından : {ctx.author}")    

    @commands.command(name = "Yardım",brief = " Komutlar hakkında bilgi verir.",aliases=["yardım"])
    async def help_command(self,ctx):
        """Help
        Use of : yardım
        """
        helpEmbed=discord.Embed(title="🤖 Komutlar",description="Komutların kullanımlarını ve işlevlerini görmek için **.help** yazabilirsin.", color=0xd8f500,timestamp=ctx.message.created_at)
        helpEmbed.add_field(name="📜 Temel",value="`Avatar`\n`Bot`\n`Evos`\n`Hesapla`\n`Ping`\n`Profil`\n`Sunucu`\n`Yardım`",inline=True)
        helpEmbed.add_field(name="🛡️ Moderasyon",value="`At`\n`Rename`\n`Sil`\n`Sustur`\n`Unban`\n`Unmute`\n`Yasakla`",inline=True)
        helpEmbed.add_field(name="🎵 Müzik",value="`Çal`\n`Çık`\n`Dur`\n`Duraklat`\n`Karıştır`\n`Liste`\n`Önceki`\n`Sıradaki`\n`Tekrarla`",inline=True)
        helpEmbed.add_field(name="⚙️ Sunucu",value="`ChangePrefix`\n`Lvmesaj`\n`ResetConfig`\n`SetAutorole`\n`Wlmesaj`",inline=True)
        helpEmbed.add_field(name="🦾 Gelişmiş",value="`Korona`\n`Kur`",inline=True)
        helpEmbed.set_footer(text=f"Talep Sahibi : {ctx.author.name}",icon_url=ctx.author.avatar_url)

        file = discord.File("images/evos.png", filename="evos.png")
        helpEmbed.set_thumbnail(url="attachment://evos.png")

        await ctx.send(file=file,embed=helpEmbed)

        logger.info(f"General | Yardım | Tarafından : {ctx.author}")

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
        statsEmbed=discord.Embed(title="📃 Bot Hakkında",color=0xd8f500,timestamp=ctx.message.created_at)
        statsEmbed.add_field(name="Evos",value=f"Python Sürümü : **{platform.python_version()}**\nDiscord.PY Sürümü : **{discord.__version__}**\nÇalışma Zamanı : **{day} Gün, {hours} Saat, {minute} Dakika, {second} Saniye**\nCPU(İşlemci) : **{get_cpu_info()['brand_raw']}**\nFiziksel Çekirdekler : **{psutil.cpu_count(logical=False)}**\nToplam Çekirdek : **{psutil.cpu_count(logical=True)}**\nOS(İşletim Sistemi) : **{platform.platform()}**\nToplam Bellek : **{get_size(svmem.total)}**\nKullanılabilir Bellek : **{get_size(svmem.available)}**\nKullanılan Bellek : **{get_size(svmem.used)}**\nKullanımdaki Bellek Yüzdesi : **%{svmem.percent}**\nBarındırılan Sunucu : **Google Cloud - Frankfurt(Almanya)**")
        statsEmbed.set_footer(text=f"Talep Sahibi : {ctx.author.name}",icon_url=ctx.author.avatar_url)
        file = discord.File("images/evos.png", filename="evos.png")
        statsEmbed.set_thumbnail(url="attachment://evos.png")
        
        await ctx.send(file=file,embed=statsEmbed)

        logger.info(f"General | BotInfo | Tarafından : {ctx.author}")

def setup(client):
    client.add_cog(General(client))