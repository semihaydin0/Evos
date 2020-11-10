import discord
from discord.utils import get
from discord.ext import commands
import requests
from bs4 import BeautifulSoup
from googletrans import Translator
import matplotlib.pyplot as coronaplt
import humanize
import os

from logging_files.requests_log import logger

class Requests(commands.Cog):
    def __init__(self,client):
        self.client = client

    @commands.command(pass_context=True ,name="Korona", brief = "COVID-19 İstatistikleri",aliases = ['korona','corona','Corona'])
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
            _t = humanize.i18n.activate("tr_TR")
            totalCases = humanize.intword(json_stats["cases"])
            if totalCases == "0":
                totalCases = "Veri girişi yok"
            todayCases = humanize.intword(json_stats["todayCases"])
            if todayCases == "0":
                todayCases = "Veri girişi yok"
            totalDeaths = humanize.intword(json_stats["deaths"])
            if totalDeaths == "0":
                totalDeaths = "Veri girişi yok"
            todayDeaths = humanize.intword(json_stats["todayDeaths"])
            if todayDeaths == "0":
                todayDeaths = "Veri girişi yok"
            recovered = humanize.intword(json_stats["recovered"])
            if recovered == "0":
                recovered = "Veri girişi yok"
            active = humanize.intword(json_stats["active"])
            if active == "0":
                active = "Veri girişi yok"
            critical = humanize.intword(json_stats["critical"])
            if critical == "0":
                critical = "Veri girişi yok"
            casesPerOneMillion = humanize.intword(json_stats["casesPerOneMillion"])
            if casesPerOneMillion == "0":
                casesPerOneMillion = "Veri girişi yok"
            totalTests = humanize.intword(json_stats["totalTests"])
            if totalTests == "0":
                totalTests = "Veri girişi yok"
            CountryNameTR = translator.translate(CountryName,dest="tr")
            TRCountry = CountryNameTR.text.title()
            Stats = discord.Embed(title=f"{TRCountry} COVID-19 İstatistikleri", colour=0xffd500, timestamp=ctx.message.created_at)
            Stats.add_field(name="Bugünkü Vaka", value=todayCases, inline=True)
            Stats.add_field(name="Bugünkü Ölüm", value=todayDeaths, inline=True)
            Stats.add_field(name="Toplam Vaka", value=totalCases, inline=True)
            Stats.add_field(name="Toplam Ölüm", value=totalDeaths, inline=True)
            Stats.add_field(name="Toplam Test", value=totalTests, inline=True)
            Stats.add_field(name="Toplam İyileşen", value=recovered, inline=True)
            Stats.add_field(name="Ağır Hasta", value=critical, inline=True)
            Stats.add_field(name="Aktif Vaka", value=active, inline=True)
            Stats.add_field(name="Bir Milyon Başına Vaka", value=casesPerOneMillion, inline=True)
            labels = ['İyileşen', 'Ölüm','Aktif']
            quantity = [Recover/Cases, Deaths/Cases,(Cases-Deaths-Recover)/Cases]
            colors = ['green', 'orangered','coral']
            explode = (0.1, 0.1, 0.1)
            coronaplt.clf()
            coronaplt.figure(figsize=(6,4),facecolor="lightgray")
            coronaplt.pie(quantity,colors=colors, explode=explode, labels=labels, autopct='%1.1f%%',shadow=True, startangle=90)
            coronaplt.axis('equal')
            coronaplt.title("Vakaların Durumlara Göre Oranı")
            coronaplt.savefig("chart.png")
            file = discord.File("chart.png", filename="image.png")
            Stats.set_image(url="attachment://image.png")
            Stats.set_thumbnail(url=CountryFlag)
            Stats.set_footer(text=f"İstek Sahibi : {ctx.author.name}",icon_url=ctx.author.avatar_url)
            await ctx.send(file=file,embed=Stats)
            os.remove("chart.png")
            logger.info(f"Requests | COVID-19 | Tarafından : {ctx.author}")
        except :
            await ctx.send("Bilinmeyen ülke adı ya da veri alınan sunucu yanıt vermiyor.Daha sonra tekrar deneyebilirsin.")

    @commands.command(pass_context=True ,name="Döviz", brief = "Anlık döviz bilgilerini getirir.",aliases = ['döviz','Kur','kur'])
    async def currency_command(self,ctx):
        try :
            Currency = requests.get('http://bigpara.hurriyet.com.tr/doviz/')
            BSoup = BeautifulSoup(Currency.content,'html.parser')
            ForeignCur = BSoup.find_all("span",{"class" :"value"})
            ForeignC = discord.Embed(title="Döviz Kuru",colour = 0xffd500,timestamp = ctx.message.created_at)
            file = discord.File("images/dollar.png", filename="dollar.png")
            ForeignC.set_thumbnail(url="attachment://dollar.png")
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
            exUSD = 1/float(USD)
            exUSD=round(exUSD,4)
            exEUR = 1/float(EUR)
            exEUR=round(exEUR,4)
            exGBP = 1/float(GBP)
            exGBP=round(exGBP,4)
            ForeignC.add_field(name=f":flag_us:    {USDPer}",value = f'1 $ = **{USD}** ₺\n1 ₺ = **{exUSD}** $')
            ForeignC.add_field(name=f":flag_eu:    {EURPer}",value = f'1 € = **{EUR}** ₺\n1 ₺ = **{exEUR}** €')
            ForeignC.add_field(name=f":flag_gb:    {GBPPer}",value = f'1 £ = **{GBP}** ₺\n1 ₺ = **{exGBP}** £')
            ForeignC.set_footer(text=f"İstek Sahibi : {ctx.author.name}",icon_url=ctx.author.avatar_url)
            await ctx.send(file=file,embed=ForeignC)
            logger.info(f"Requests | Kur | Tarafından : {ctx.author}")
        except :
            await ctx.send("Veri alınan sunucu yanıt vermiyor.Daha sonra tekrar deneyebilirsin.")
        
def setup(client):
    client.add_cog(Requests(client))