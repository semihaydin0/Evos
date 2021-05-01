#MIT License
#Copyright (c) 2020 Semih Aydın
#UTF-8

import discord
from discord.ext import commands
import matplotlib.pyplot as coronaplt
from googletrans import Translator
from bs4 import BeautifulSoup
import cryptocompare
import TenGiphPy
import requests
import humanize
import os
from logging_files.requests_log import logger

class Requests(commands.Cog):
    def __init__(self,client):
        self.client = client

    @commands.cooldown(1, 30, commands.BucketType.user)
    @commands.command(name="Korona", brief = "Detaylı COVID-19 istatistiklerini görüntüler.",aliases = ['korona','corona','Corona'])
    async def corona_command(self,ctx,CountryName = None):
        try :
            if CountryName is None :
                CountryName = "dünya"

            translator = Translator()
            translation = translator.translate(CountryName)
            Country = translation.text.title()
            DataUrl = f"https://coronavirus-19-api.herokuapp.com/countries/{Country}"

            if Country == "World" :
                CountryFlag = "https://i.ibb.co/fVJyrgP/world.png"

            else :
                CountryFlag = f"https://www.countries-ofthe-world.com/flags-normal/flag-of-{Country}.png"

            stats = requests.get(DataUrl)
            json_stats = stats.json()
            Cases = json_stats["cases"]
            Recover = json_stats["recovered"]
            Deaths = json_stats["deaths"]
            humanize.i18n.activate("tr_TR")
            totalCases = humanize.intword(json_stats["cases"])
            todayCases = humanize.intword(json_stats["todayCases"])
            totalDeaths = humanize.intword(json_stats["deaths"])
            todayDeaths = humanize.intword(json_stats["todayDeaths"])
            recovered = humanize.intword(json_stats["recovered"])
            active = humanize.intword(json_stats["active"])
            critical = humanize.intword(json_stats["critical"])
            casesPerOneMillion = humanize.intword(json_stats["casesPerOneMillion"])
            totalTests = humanize.intword(json_stats["totalTests"])

            if totalCases == "0":
                totalCases = "Veri girişi yok"

            if todayCases == "0":
                todayCases = "Veri girişi yok"

            if totalDeaths == "0":
                totalDeaths = "Veri girişi yok"

            if todayDeaths == "0":
                todayDeaths = "Veri girişi yok"

            if recovered == "0":
                recovered = "Veri girişi yok"

            if active == "0":
                active = "Veri girişi yok"

            if critical == "0":
                critical = "Veri girişi yok"

            if casesPerOneMillion == "0":
                casesPerOneMillion = "Veri girişi yok"

            if totalTests == "0":
                totalTests = "Veri girişi yok"

            CountryNameTR = translator.translate(CountryName,dest="tr")
            TRCountry = CountryNameTR.text.title()
            coronaStatsEmbed = discord.Embed(title=f"{TRCountry} COVID-19 İstatistikleri", colour=0xffd500, timestamp=ctx.message.created_at)
            coronaStatsEmbed.add_field(name="Bugünkü Vaka", value=todayCases)
            coronaStatsEmbed.add_field(name="Bugünkü Ölüm", value=todayDeaths)
            coronaStatsEmbed.add_field(name="Toplam Vaka", value=totalCases)
            coronaStatsEmbed.add_field(name="Toplam Ölüm", value=totalDeaths)
            coronaStatsEmbed.add_field(name="Toplam Test", value=totalTests)
            coronaStatsEmbed.add_field(name="Toplam İyileşen", value=recovered)
            coronaStatsEmbed.add_field(name="Ağır Hasta", value=critical)
            coronaStatsEmbed.add_field(name="Aktif Vaka", value=active)
            coronaStatsEmbed.add_field(name="Bir Milyon Başına Vaka", value=casesPerOneMillion)

            labels = ['İyileşen', 'Ölen','Aktif']
            quantity = [Recover/Cases, Deaths/Cases,(Cases-Deaths-Recover)/Cases]
            explodeValue = 0.2

            if max(quantity) >= 0.9 :
                explodeValue = 0.4

            elif max(quantity) >= 0.8 :
                explodeValue = 0.3

            colors = ['green', 'orangered','coral']
            explode = (explodeValue, explodeValue, explodeValue)
            coronaplt.clf()
            coronaplt.figure(figsize=(6,4),facecolor="lightgray")
            coronaplt.pie(quantity,colors=colors, explode=explode, labels=labels, autopct='%1.1f%%',shadow=True, startangle=90)
            coronaplt.axis('equal')
            coronaplt.title("VAKALARIN DURUMLARI")
            coronaplt.savefig(f"{ctx.author.id}.png")

            file = discord.File(f"{ctx.author.id}.png", filename=f"{Country}_COVID-19.png")

            coronaStatsEmbed.set_image(url=f"attachment://{Country}_COVID-19.png")
            coronaStatsEmbed.set_thumbnail(url=CountryFlag)
            coronaStatsEmbed.set_footer(text=f"Tarafından: {ctx.author}",icon_url=ctx.author.avatar_url)

            await ctx.send(file=file,embed=coronaStatsEmbed)

            os.remove(f"{ctx.author.id}.png")

            logger.info(f"Requests | COVID-19 | Tarafından: {ctx.author}")
        except Exception as e:
            coronaStatsEmbed_2 = discord.Embed(title="Hata",description ="Bilinmeyen ülke adı ya da veri sunucusu yanıt vermiyor.",colour = 0xd92929)
            await ctx.send(embed=coronaStatsEmbed_2)

            logger.error(f"Requests | COVID-19 | Error: {e}")

    @commands.cooldown(1, 30, commands.BucketType.user)
    @commands.command(name="Kur", brief = "Canlı döviz kurunu görüntüler.",aliases = ['döviz','Döviz','kur'])
    async def currency_command(self,ctx):
        try :
            Currency = requests.get('http://bigpara.hurriyet.com.tr/doviz/')
            BSoup = BeautifulSoup(Currency.content,'html.parser')
            ForeignCur = BSoup.find_all("span",{"class" :"value"})

            USD = ForeignCur[2].text.replace(",",".")
            EUR = ForeignCur[5].text.replace(",",".")
            GBP = ForeignCur[8].text.replace(",",".")

            USDPer=ForeignCur[0].text
            EURPer=ForeignCur[3].text
            GBPPer=ForeignCur[6].text

            if USDPer.startswith('-') == False:
                USDPer = f"+{USDPer}"

            if EURPer.startswith('-') == False:
                EURPer = f"+{EURPer}"

            if GBPPer.startswith('-') == False:
                GBPPer = f"+{GBPPer}"

            exUSD=round(1/float(USD),4)
            exEUR=round(1/float(EUR),4)
            exGBP=round(1/float(GBP),4)

            file = discord.File("images/dollar.png", filename="dollar.png")

            currencyEmbed = discord.Embed(title="Canlı Döviz Kuru",colour = 0x36393F,timestamp = ctx.message.created_at)
            currencyEmbed.set_thumbnail(url="attachment://dollar.png")
            currencyEmbed.add_field(name=f":flag_us:    {USDPer}",value = f'1 $ = **{USD}** ₺\n1 ₺ = **{exUSD}** $')
            currencyEmbed.add_field(name=f":flag_eu:    {EURPer}",value = f'1 € = **{EUR}** ₺\n1 ₺ = **{exEUR}** €')
            currencyEmbed.add_field(name=f":flag_gb:    {GBPPer}",value = f'1 £ = **{GBP}** ₺\n1 ₺ = **{exGBP}** £')
            currencyEmbed.set_footer(text=f"Tarafından: {ctx.author}",icon_url=ctx.author.avatar_url)

            await ctx.send(file=file,embed=currencyEmbed)

            logger.info(f"Requests | Kur | Tarafından: {ctx.author}")
        except Exception as e:
            currencyEmbed_2 = discord.Embed(title="Hata",description =f"{e}",colour = 0xd92929)
            await ctx.send(embed=currencyEmbed_2)

            logger.error(f"Requests | Kur | Error: {e}")

    @commands.cooldown(1, 15, commands.BucketType.user)
    @commands.command(name="Kripto", brief = "Canlı kripto çitflerinin bilgilerini görüntüler.",aliases = ['kripto','Coin','coin'])
    async def crypto_command(self,ctx,fromSymbol:str,toSymbol:str):
        try:
            data = cryptocompare.get_price(fromSymbol, currency=toSymbol, full=True)
        except Exception as e:
            cryptoEmbed = discord.Embed(title="Hata",description ="Bilinmeyen indeks ya da veri sunucusu yanıt vermiyor.",colour = 0xd92929)
            await ctx.send(embed=cryptoEmbed)

            logger.error(f"Requests | Kripto | Error: {e}")
            return

        fs = fromSymbol.upper()
        ts = toSymbol.upper()
        humanize.i18n.activate("tr_TR")

        price = data['RAW'][fs][ts]['PRICE']
        changepct24hour = data['RAW'][fs][ts]['CHANGEPCT24HOUR']
        changeday = data['RAW'][fs][ts]['CHANGEDAY']
        low24hour = data['RAW'][fs][ts]['LOW24HOUR']
        high24hour = data['RAW'][fs][ts]['HIGH24HOUR']
        marketcap = data['RAW'][fs][ts]['MKTCAP']

        file = discord.File("images/cclogo.png", filename="cclogo.png")

        cryptoEmbed_2 = discord.Embed(title=f"{fs}/{ts}",description="Veriler **CryptoCompare** tarafından sağlanmaktadır.",colour=0x36393F, timestamp=ctx.message.created_at)
        cryptoEmbed_2.set_thumbnail(url="attachment://cclogo.png")
        cryptoEmbed_2.add_field(name="Fiyat",value=f"**{round(price,5)}** {ts}")
        cryptoEmbed_2.add_field(name="24H Değişim Yüzdesi",value=f"**{round(changepct24hour,2)}**%")
        cryptoEmbed_2.add_field(name="24H Değişim Değeri",value=f"**{round(changeday,5)}** {ts}")
        cryptoEmbed_2.add_field(name="24H En Düşük",value=f"**{round(low24hour,5)}** {ts}")
        cryptoEmbed_2.add_field(name="24H En Yüksek",value=f"**{round(high24hour,5)}** {ts}")
        cryptoEmbed_2.add_field(name="Market Cap",value=f"**{humanize.intword(marketcap)}** {ts}")
        cryptoEmbed_2.set_footer(text=f"Tarafından: {ctx.author}",icon_url=ctx.author.avatar_url)

        await ctx.send(file=file,embed=cryptoEmbed_2)

        logger.info(f"Requests | Kripto | Tarafından: {ctx.author}")

    @commands.cooldown(1, 5, commands.BucketType.user)
    @commands.command(name="Gif",brief="Tenor GIF servisi.",aliases=["gif"])
    async def gif_command(self,ctx, *,tag: str):
        try:
            apiToken = "YOURAPITOKENGOESHERE"
            t = TenGiphPy.Tenor(token=apiToken)
            randomGif = t.random(tag=tag)

            gifEmbed=discord.Embed(title=f"#{tag}",color=0x36393F)
            gifEmbed.set_image(url=randomGif)
            gifEmbed.set_footer(text=f"Tarafından: {ctx.author}",icon_url=ctx.author.avatar_url)

            await ctx.send(embed=gifEmbed)

            logger.info(f"Requests | Gif | Tarafından: {ctx.author}")
        except Exception as e:
            gifEmbed_2 = discord.Embed(title="Hata",description =f"{e}",colour = 0xd92929)
            await ctx.send(embed=gifEmbed_2)

            logger.error(f"Requests | Gif | Error: {e}")

def setup(client):
    client.add_cog(Requests(client))