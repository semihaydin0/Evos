#MIT License
#Copyright (c) 2020 Semih Aydın
#UTF-8

import discord
from discord.ext import commands
from cpuinfo import get_cpu_info
from uptime import uptime
import speedtest
import platform
import asyncio
import random
import psutil
import math
import time
from pyfiglet import Figlet
from pyfiglet import FigletFont
from logging_files.general_log import logger
from Evos import get_version_number

def get_size(bts, suffix="B"):
    factor = 1024
    for unit in ["", "K", "M", "G", "T", "P"]:
        if bts < factor:
            return f"{bts:.2f}{unit}{suffix}"
        bts /= factor

class General(commands.Cog):
    def __init__(self,client):
        self.client = client

    @commands.cooldown(1, 10, commands.BucketType.user)
    @commands.command(name ="Ping",brief ="Evos'un gecikme değerlerini gösterir.",aliases = ['ping','Latency','latency'])
    async def ping_command(self,ctx):
        before = time.monotonic()
        pingEmbed = discord.Embed(title="Ölçülüyor...",color=0x36393F)
        msg = await ctx.send(embed=pingEmbed)
        ping = (time.monotonic() - before) * 1000
        pingEmbed_2 = discord.Embed(title = "Gecikme Süreleri",color=0x36393F)
        pingEmbed_2.add_field(name="API Gecikmesi",value=f"{round(self.client.latency * 1000)} ms",inline=False)
        pingEmbed_2.add_field(name="Mesaj Gecikmesi",value=f"{round(ping)} ms")
        pingEmbed_2.set_footer(text=f"Tarafından: {ctx.author}",icon_url=ctx.author.avatar_url)

        await msg.edit(embed=pingEmbed_2)

        logger.info(f"General | Ping | Tarafından: {ctx.author}")

    @commands.guild_only()
    @commands.cooldown(1, 30, commands.BucketType.guild)
    @commands.command(name ="Davet",brief ="Kanal davet linki oluşturur.",aliases=['davet','Invite','invite'])
    async def invite_command(self,ctx,time: int = 0,amount: int = 0):
        link = await ctx.channel.create_invite(max_age = time*3600,max_uses = amount)

        if time == 0:
            time = "Süresiz"
        else:
            time = str(time)+" saat"

        if amount == 0:
            amount = "Limitsiz"

        inviteEmbed=discord.Embed(description =f"Davet Linki: {link}\nBu davetin **geçerlilik** süresi: {time}\nBu davetin **maksimum kullanım** sayısı: {amount}",color=0xd8f500,timestamp=ctx.message.created_at)
        inviteEmbed.set_author(name=ctx.message.guild.name,icon_url=ctx.message.guild.icon_url)
        inviteEmbed.set_footer(text=f"Tarafından: {ctx.author}",icon_url=ctx.author.avatar_url)

        await ctx.send(embed=inviteEmbed)

        logger.info(f"General | Invite | Tarafından: {ctx.author}")

    @commands.command(name ="Evos",brief ="Botun davet linkini gönderir.",aliases=["evos"])
    async def evos_invite_command(self,ctx):
        evosEmbed=discord.Embed(title =f"{self.client.user.name} | Türkçe Discord Botu",color=0x36393F,timestamp=ctx.message.created_at)
        evosEmbed.add_field(name="Davet Linki",value=f"[Buradan](https://discord.com/api/oauth2/authorize?client_id={self.client.user.id}&permissions=8&scope=bot) sunucuna ekleyebilirsin.",inline=False)
        evosEmbed.add_field(name="Geliştirici misin ?",value="[Buradan](https://github.com/semihaydin0/Evos) kaynak kodlarını inceleyebilirsin.")

        file = discord.File("images/evos.png", filename="evos.png")
        evosEmbed.set_thumbnail(url="attachment://evos.png")
        evosEmbed.set_footer(text=f"Tarafından: {ctx.author}",icon_url=ctx.author.avatar_url)

        await ctx.send(file=file,embed=evosEmbed)

        logger.info(f"General | Evos | Tarafından: {ctx.author}")

    @commands.command(name="Hesapla",brief="İki sayı ile dört işlem yapar.",aliases = ['hesapla','Math','math'])
    async def math_command(self,ctx,num1: float,op: str,num2: float):
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
            mathEmbed_2 = discord.Embed(title="Hata",description="Hatalı operatör girişi.\nDesteklenen Operatörler: **+ - * /**",color=0xd92929)

            await ctx.send(embed=mathEmbed_2)
            return

        mathEmbed = discord.Embed(title="Sonuç",description=f"{num1}{op}{num2} işleminin sonucu = **{result}**",color=0xd8f500)
        mathEmbed.set_footer(text=f"Tarafından: {ctx.author}",icon_url=ctx.author.avatar_url)

        await ctx.send(embed=mathEmbed)

        logger.info(f"General | Math | Tarafından: {ctx.author}")

    @commands.command(name ="Yardım",brief ="Komutlar hakkında bilgi verir.",aliases=["yardım"])
    async def help_command(self,ctx,cog="1"):
        helpEmbed=discord.Embed(title="🤖 Komutlar",description="Komutlar için gerekli argümanlara **help** komutuyla ulaşabilirsin.", color=0xd8f500,timestamp=ctx.message.created_at)
        file = discord.File("images/evos.png", filename="evos.png")
        helpEmbed.set_thumbnail(url="attachment://evos.png")
        tempC = cog

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

        neededCogs = []

        for i in range(4):
            x = i + (int(cog) - 1) * 4
            try:
                neededCogs.append(cogs[x])
            except IndexError:
                pass

        commandCount = 0
        for cog in neededCogs:
            commandList = ""

            for command in self.client.get_cog(cog).walk_commands():
                if command.hidden:
                    continue
                elif command.parent != None:
                    continue
                commandList += f"**{command.name}** - *{command.brief}*\n"
                commandCount += 1
            commandList += "\n"
            helpEmbed.add_field(name=cog, value=commandList, inline=False)

        helpEmbed.set_footer(text=f"{tempC}.Sayfa | Toplam Sayfa: {totalPages} | Bu Sayfadaki Toplam Komut Sayısı: {commandCount}")
        await ctx.send(file=file,embed=helpEmbed)

        logger.info(f"General | Help | Tarafından: {ctx.author}")

    @commands.cooldown(1, 60, commands.BucketType.user)
    @commands.command(name="Evosinfo",brief="Evos'un istatistiklerini gösterir.",aliases=["evosinfo"])
    async def info_command(self,ctx):
        svmem = psutil.virtual_memory()
        day = int(uptime()/3600/24)
        hours = int(uptime()/3600-day*24)
        minute = int(uptime()/60)-day*24*60-hours*60
        second = int(uptime())-day*24*3600-hours*3600-minute*60

        statsEmbed=discord.Embed(title=f"📃 {self.client.user.name} Hakkında",color=0xd8f500,timestamp=ctx.message.created_at)
        statsEmbed.add_field(name="Teknik Bilgiler",value=f"{self.client.user.name} Versiyonu: **v{get_version_number()}**\nPython Versiyonu: **{platform.python_version()}**\nDiscord.py Versiyonu: **{discord.__version__}**\nÇalışma Zamanı: **{day} Gün, {hours} Saat, {minute} Dakika, {second} Saniye**\nCPU(İşlemci): **{get_cpu_info()['brand_raw']}**\nFiziksel Çekirdekler: **{psutil.cpu_count(logical=False)}**\nToplam Çekirdek: **{psutil.cpu_count(logical=True)}**\nKullanımdaki İşlemci Yüzdesi: **%{psutil.cpu_percent(interval=0)}**\nOS(İşletim Sistemi): **{platform.platform()}**\nKullanılan Bellek: **{get_size(svmem.used)}**\nKullanılabilir Bellek: **{get_size(svmem.available)}**\nToplam Bellek: **{get_size(svmem.total)}**\nKullanımdaki Bellek Yüzdesi: **%{svmem.percent}**\nSunucu Bölgesi: **Google Cloud - Frankfurt**")
        statsEmbed.set_footer(text="PHOENIX#7103 tarafından 💖 ile geliştirildi!",icon_url=ctx.author.avatar_url)

        file = discord.File("images/evos.png", filename="evos.png")
        statsEmbed.set_thumbnail(url="attachment://evos.png")

        await ctx.send(file=file,embed=statsEmbed)

        logger.info(f"General | Evosinfo | Tarafından: {ctx.author}")

    @commands.guild_only()
    @commands.cooldown(1, 300, commands.BucketType.guild)
    @commands.command(name="Speedtest",brief="Evos'un barındığı sunucunun internet hızını gösterir.",aliases=["speedtest","Hıztesti","hıztesti"])
    async def speedtest_command(self,ctx):
        try:
            st = speedtest.Speedtest()
            st.get_best_server()
            asyncio.get_event_loop()

            speedtestEmbed=discord.Embed(title="Hız Testi Ölçümü",color=0x36393F)
            speedtestEmbed.add_field(name="İndirme (Ölçülüyor)",value=":yellow_circle:",inline=False)
            speedtestEmbed.add_field(name="Yükleme",value=":red_circle:")
            speedtestEmbed.set_footer(text=f"Tarafından: {ctx.author}",icon_url=ctx.author.avatar_url)

            message = await ctx.send(embed=speedtestEmbed)

            d = await self.client.loop.run_in_executor(None, st.download)

            speedtestEmbed_2=discord.Embed(title="Hız Testi Ölçümü",color=0x36393F)
            speedtestEmbed_2.add_field(name="İndirme (Tamamlandı)",value=":green_circle:",inline=False)
            speedtestEmbed_2.add_field(name="Yükleme (Ölçülüyor)",value=":yellow_circle:")
            speedtestEmbed_2.set_footer(text=f"Tarafından: {ctx.author}",icon_url=ctx.author.avatar_url)

            await message.edit(embed=speedtestEmbed_2)

            u = await self.client.loop.run_in_executor(None, st.upload)

            speedtestEmbed_3=discord.Embed(title="Hız Testi Sonuçları",color=0x36393F)
            speedtestEmbed_3.add_field(name="İndirme",value=f"**{round(d/1024/1024, 2)}** Mbps",inline=False)
            speedtestEmbed_3.add_field(name="Yükleme",value=f"**{round(u/1024/1024, 2)}** Mbps")
            speedtestEmbed_3.add_field(name="Ping",value=f"**{round(st.results.ping, 2)}** ms",inline=False)
            speedtestEmbed_3.set_footer(text=f"Tarafından: {ctx.author}",icon_url=ctx.author.avatar_url)

            await message.edit(embed=speedtestEmbed_3)

            logger.info(f"General | Speedtest | Tarafından: {ctx.author}")
        except Exception as e:
            speedtestEmbed_4 = discord.Embed(title="Hata",description =f"{e}",colour = 0xd92929)
            await ctx.send(embed=speedtestEmbed_4)

            logger.error(f"General | Speedtest | Error: {e}")

    @commands.cooldown(1, 5, commands.BucketType.user)
    @commands.command(name="Ascii",brief="Girmiş olduğunuz metni ascii metnine çevirir.",aliases=["ascii"])
    async def ascii_command(self,ctx, *,text: str):
        try:
            font = 'slant'

            f = Figlet(font=font)
            out = f.renderText(text)
            await ctx.send(f"```\n{out}\n```")

            logger.info(f"General | Ascii | Tarafından: {ctx.author}")
        except Exception as e:
            asciiEmbed = discord.Embed(title="Hata",description =f"{e}",colour = 0xd92929)
            await ctx.send(embed=asciiEmbed)

            logger.error(f"General | Ascii | Error: {e}")

    @commands.cooldown(1, 5, commands.BucketType.user)
    @commands.command(name="Asciirandom",brief="Girmiş olduğunuz metni ascii metnine çevirir.",aliases=["asciirandom"])
    async def ascii_random_command(self,ctx, *,text: str):
        try:
            fonts = FigletFont.getFonts()
            font = random.choice(fonts)

            f = Figlet(font=font)
            out = f.renderText(text)
            await ctx.send(f"```\n{out}\n```")

            logger.info(f"General | AsciiRandom | Tarafından: {ctx.author}")
        except Exception as e:
            asciiRandomEmbed = discord.Embed(title="Hata",description =f"{e}",colour = 0xd92929)
            await ctx.send(embed=asciiRandomEmbed)

            logger.error(f"General | AsciiRandom | Error: {e}")

def setup(client):
    client.add_cog(General(client))