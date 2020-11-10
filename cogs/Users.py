import discord
from discord.utils import get
from discord.ext import commands
import datetime

from logging_files.users_log import logger

class Users(commands.Cog):
    def __init__(self,client):
        self.client = client

    @commands.guild_only()
    @commands.command(pass_context=True ,name="Profil", brief = "Kullanıcının profil bilgilerini getirir.",aliases = ['profil'])
    async def profile_command(self,ctx,member : discord.Member = None):
        if member is None :
             member = ctx.message.author
        Profile = discord.Embed(colour=0xd8f500, timestamp=ctx.message.created_at)
        Profile.set_author(name=member,icon_url=member.avatar_url)
        Profile.set_thumbnail(url=member.avatar_url)
        Profile.add_field(name="Kayıt Tarihi", value=member.created_at.strftime("%#d/%m/%Y"),inline=True)
        Profile.add_field(name="Katılma Tarihi", value=member.joined_at.strftime("%#d/%m/%Y"),inline=True)
        if member.premium_since != None :
            Profile.add_field(name="Sunucu Desteği Tarihi", value=member.premium_since.strftime("%#d/%m/%Y"),inline=False)
        roles = [role for role in member.roles]
        Profile.add_field(name=f"Roller [{len(roles)}]", value=" ".join([role.mention for role in roles]),inline=False) 
        Profile.add_field(name=f"En Yüksek Rolü", value=member.top_role.mention,inline=True)
        status = "Hayır"
        if member.bot == True :
            status = "Evet"
        Profile.add_field(name=f"Bot mu?", value=status,inline=True)
        file = discord.File("images/evos.png", filename="evos.png")
        Profile.set_footer(text=f"Kullanıcı ID:{member.id}",icon_url="attachment://evos.png")
        await ctx.send(file=file,embed=Profile)
        logger.info(f"Users | Profil | Tarafından : {ctx.author}")
    
    @commands.guild_only()
    @commands.command(pass_context=True ,name="Avatar",brief = "Kullanıcının avatarını getirir.",aliases = ['avatar'])
    async def avatar_command(self,ctx,member : discord.Member=None):
        AvatarEmbed = discord.Embed()
        if member is None :
           AvatarEmbed.set_author(name = ctx.message.author)
           AvatarEmbed.set_image(url = f'{ctx.message.author.avatar_url}')
        else :
            AvatarEmbed.set_author(name = member)
            AvatarEmbed.set_image(url = f'{member.avatar_url}')
        await ctx.send(embed=AvatarEmbed)
        logger.info(f"Users | Avatar | Tarafından : {ctx.author}")

    @commands.guild_only()
    @commands.command(pass_context=True ,name="Sunucu", brief = "Server bilgilerini getirir.",aliases = ['sunucu'])
    async def server_command(self,ctx):
        ServerE = discord.Embed(colour=0xffd500, timestamp=ctx.message.created_at)
        ServerE.set_author(name=ctx.message.guild.name,icon_url=ctx.message.guild.icon_url)
        ServerE.set_thumbnail(url=ctx.message.guild.icon_url)
        ServerE.add_field(name="Sahibi", value=ctx.author.guild.owner,inline=True)
        ServerE.add_field(name="Açılış Tarihi", value=ctx.message.guild.created_at.strftime("%#d/%m/%Y"),inline=True)
        ServerE.add_field(name="Bölge", value=ctx.author.guild.region,inline=True)
        countBot = 0
        countHuman = 0
        for member in ctx.author.guild.members :
            if member.bot==True :
                countBot +=1
            else :
                countHuman +=1
        ServerE.add_field(name="Kanal Sayıları", value=f"Metin : {len(ctx.author.guild.text_channels)}\nSes : {len(ctx.author.guild.voice_channels)}\nKategori : {len(ctx.author.guild.categories)}",inline=True)        
        ServerE.add_field(name="Üye Sayıları", value=f"İnsan : {countHuman}\nBot : {countBot}",inline=True)
        ServerE.add_field(name="Rol Sayısı", value=f"{len(ctx.guild.roles)}",inline=True)
        ServerE.add_field(name="Takviye Seviyesi", value=ctx.author.guild.premium_tier,inline=True)
        ServerE.add_field(name="Takviye Sayısı", value=ctx.author.guild.premium_subscription_count,inline=True)
        file = discord.File("images/evos.png", filename="evos.png")
        ServerE.set_footer(text=f"Sunucu ID:{ctx.message.guild.id}",icon_url="attachment://evos.png")
        await ctx.send(file=file,embed=ServerE)
        logger.info(f"Users | Sunucu Bilgileri : {ctx.author.guild.name} | Tarafından : {ctx.author}")

def setup(client):
    client.add_cog(Users(client))