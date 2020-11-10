import discord
from discord.utils import get
from discord.ext import commands

from logging_files.general_log import logger

class General(commands.Cog):
    def __init__(self,client):
        self.client = client

    @commands.command(name = "Ping",brief = "Evos'un gecikme değerini gösterir.",aliases = ["latency","ping"])
    async def ping_command(self,ctx):
        PingEmbed = discord.Embed(title = f'Ping : {round(self.client.latency * 1000)} ms',color=0xd8f500)
        PingEmbed.set_footer(text=f"Talep Sahibi : {ctx.author.name}",icon_url=ctx.author.avatar_url)
        await ctx.send(embed=PingEmbed)
        logger.info(f"General | Ping : {round(self.client.latency * 1000)} ms  | Tarafından : {ctx.author}")

    @commands.guild_only()
    @commands.command(name = "Davet",brief = "Sunucu davet linki oluşturur.",aliases=["davet"])
    async def guild_invite_command(self,ctx):
        link = await ctx.channel.create_invite(max_age = 300)
        GuildInvt=discord.Embed(description =f"**Davet Linki** : {link}" ,color=0xd8f500)
        GuildInvt.set_author(name=ctx.message.guild.name,icon_url=ctx.message.guild.icon_url)
        GuildInvt.set_footer(text=f"Talep Sahibi : {ctx.author.name}",icon_url=ctx.author.avatar_url)
        await ctx.send(embed=GuildInvt)
        logger.info(f"General | Sunucu Daveti : {ctx.guild.name} | Tarafından : {ctx.author}")

    @commands.command(name = "Evos",brief = "Evos'un davet linkini gönderir.",aliases=["evos"])
    async def evos_invite_command(self,ctx):
        evosinviteEmbed=discord.Embed(title =f"Evos - Türkçe Discord Botu",description ="**Bu [linke](https://discord.com/api/oauth2/authorize?client_id=675459603420545056&permissions=8&scope=bot)** tıklayarak beni sunucuna ekleyebilirsin." ,color=0xd8f500,timestamp=ctx.message.created_at)
        evosinviteEmbed.add_field(name="Kaynak Kodları",value="https://github.com/semihaydin0/Evos")
        file = discord.File("images/evos.png", filename="evos.png")
        evosinviteEmbed.set_footer(text=f"Teşekkürler !",icon_url="attachment://evos.png")
        await ctx.send(file=file,embed=evosinviteEmbed)
        logger.info(f"General | Bot Daveti | Tarafından : {ctx.author}")

    @commands.command(name = "Yardım",brief = " Komutlar hakkında bilgi verir.",aliases=["yardım"])
    async def help_command(self,ctx):
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

def setup(client):
    client.add_cog(General(client))