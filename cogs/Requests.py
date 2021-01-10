#MIT License
#Copyright (c) 2020 Semih Aydın
#UTF-8

import discord
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
        # Info : The country argument of this command supports all languages.The display language is Turkish.
        """COVID-19 Statistics
        Use of : corona {country}
        """

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
                try :
                    CountryFlag = f"https://www.countries-ofthe-world.com/flags-normal/flag-of-{Country}.png"
                except :
                    pass

            stats = requests.get(DataUrl)
            json_stats = stats.json()
            Cases = json_stats["cases"]
            Recover = json_stats["recovered"]
            Deaths = json_stats["deaths"]
            _t = humanize.i18n.activate("tr_TR")

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
            coronaStatsEmbed.add_field(name="Bugünkü Vaka", value=todayCases, inline=True)
            coronaStatsEmbed.add_field(name="Bugünkü Ölüm", value=todayDeaths, inline=True)
            coronaStatsEmbed.add_field(name="Toplam Vaka", value=totalCases, inline=True)
            coronaStatsEmbed.add_field(name="Toplam Ölüm", value=totalDeaths, inline=True)
            coronaStatsEmbed.add_field(name="Toplam Test", value=totalTests, inline=True)
            coronaStatsEmbed.add_field(name="Toplam İyileşen", value=recovered, inline=True)
            coronaStatsEmbed.add_field(name="Ağır Hasta", value=critical, inline=True)
            coronaStatsEmbed.add_field(name="Aktif Vaka", value=active, inline=True)
            coronaStatsEmbed.add_field(name="Bir Milyon Başına Vaka", value=casesPerOneMillion, inline=True)

            labels = ['İyileşen', 'Ölen','Aktif']
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

            coronaStatsEmbed.set_image(url="attachment://image.png")
            coronaStatsEmbed.set_thumbnail(url=CountryFlag)
            coronaStatsEmbed.set_footer(text=f"Tarafından : {ctx.author.name}",icon_url=ctx.author.avatar_url)

            await ctx.send(file=file,embed=coronaStatsEmbed)

            os.remove("chart.png")

            logger.info(f"Requests | COVID-19 | Tarafından : {ctx.author}")
        except :
            coronaStatsErrorEmbed = discord.Embed(title="Hata",description ="Bilinmeyen ülke adı ya da veri sunucusu yanıt vermiyor.",colour = 0xffd500)
            await ctx.send(embed=coronaStatsErrorEmbed)

    @commands.command(pass_context=True ,name="Kur", brief = "Anlık döviz bilgilerini getirir.",aliases = ['döviz','Döviz','kur'])
    async def currency_command(self,ctx):
        """The value of the Turkish lira against other currencies and cryptocurrencies
        Use of : kur
        """

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

            CryptoBTC = requests.get('https://bitcoin.tlkur.com/')
            BSoup = BeautifulSoup(CryptoBTC.content,'html.parser')
            BTCCur = BSoup.find("span",{"id" :"BTCTL_rate"})
            
            CryptoETH = requests.get('https://ethereum.tlkur.com/')
            BSoup = BeautifulSoup(CryptoETH.content,'html.parser')
            ETHCur = BSoup.find("span",{"id" :"ETHTL_rate"})
            
            CryptoXRP = requests.get('https://ripple.tlkur.com/')
            BSoup = BeautifulSoup(CryptoXRP.content,'html.parser')
            XRPCur = BSoup.find("span",{"id" :"XRPTL_rate"})

            BTC = round(float(BTCCur.text),2)
            ETH = round(float(ETHCur.text),2)
            XRP = round(float(XRPCur.text),2)

            currencyEmbed = discord.Embed(title="Canlı Döviz Kuru ve Kripto Paralar",colour = 0xffd500,timestamp = ctx.message.created_at)
            
            file = discord.File("images/dollar.png", filename="dollar.png")
            
            currencyEmbed.set_thumbnail(url="attachment://dollar.png")
            currencyEmbed.add_field(name=f":flag_us:    {USDPer}",value = f'1 $ = **{USD}** ₺\n1 ₺ = **{exUSD}** $')
            currencyEmbed.add_field(name=f":flag_eu:    {EURPer}",value = f'1 € = **{EUR}** ₺\n1 ₺ = **{exEUR}** €')
            currencyEmbed.add_field(name=f":flag_gb:    {GBPPer}",value = f'1 £ = **{GBP}** ₺\n1 ₺ = **{exGBP}** £')
            currencyEmbed.add_field(name=f"Bitcoin",value = f'1 ₿ = **{BTC}** ₺\n1 ₺ = **{round(1/float(BTC),7)}** ₿')
            currencyEmbed.add_field(name=f"Ethereum",value = f'1 Ξ = **{ETH}** ₺\n1 ₺ = **{round(1/float(ETH),6)}** Ξ')
            currencyEmbed.add_field(name=f"Ripple",value = f'1 X = **{XRP}** ₺\n1 ₺ = **{round(1/float(XRP),2)}** X')
            currencyEmbed.set_footer(text=f"Tarafından : {ctx.author.name}",icon_url=ctx.author.avatar_url)
            
            await ctx.send(file=file,embed=currencyEmbed)
            
            logger.info(f"Requests | Kur | Tarafından : {ctx.author}")
        except :
            currencyErrorEmbed = discord.Embed(title="Hata",description ="Veri sunucusu yanıt vermiyor.",colour = 0xffd500)
            await ctx.send(embed=currencyErrorEmbed)
        
def setup(client):
    client.add_cog(Requests(client))