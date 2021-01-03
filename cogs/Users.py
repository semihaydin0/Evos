#MIT License
#Copyright (c) 2020 Semih Aydın
#UTF-8

import discord
from discord.ext import commands

from logging_files.users_log import logger

class Users(commands.Cog):
    def __init__(self,client):
        self.client = client

    @commands.guild_only()
    @commands.command(name="Profil", brief = "Kullanıcının profil bilgilerini getirir.",aliases = ['profil'])
    async def profile_command(self,ctx,member : discord.Member = None):
        """Profile
        Use of : profil
        """
        if member is None :
             member = ctx.message.author
        Profile = discord.Embed(colour=member.color, timestamp=ctx.message.created_at)
        Profile.set_author(name=member,icon_url=member.avatar_url)
        Profile.set_thumbnail(url=member.avatar_url)
        Profile.add_field(name="Kayıt Tarihi", value=member.created_at.strftime("`%#d/%m/%Y`"),inline=True)
        Profile.add_field(name="Katılma Tarihi", value=member.joined_at.strftime("`%#d/%m/%Y`"),inline=True)
        roles = [role for role in member.roles]
        Profile.add_field(name=f"Roller [`{len(roles)}`]", value=" ".join([role.mention for role in roles]),inline=False)
        
        if member.premium_since != None :
            Profile.add_field(name="Sunucu Desteği Tarihi", value=member.premium_since.strftime("`%#d/%m/%Y`"),inline=False)
        Profile.set_footer(text=f"Profil ID: {member.id}")
        
        await ctx.send(embed=Profile)
        
        logger.info(f"Users | Profil | Tarafından : {ctx.author}")
    
    @commands.command(name="Avatar",brief = "Kullanıcının avatarını getirir.",aliases = ['avatar'])
    async def avatar_command(self,ctx,member : discord.Member=None):
        """Avatar
        Use of : avatar
        """
        if member is None : 
            member = ctx.message.author
        AvatarEmbed = discord.Embed(colour=member.color)
        AvatarEmbed.set_author(name = member)
        AvatarEmbed.set_image(url = f'{member.avatar_url}')
        
        await ctx.send(embed=AvatarEmbed)
        
        logger.info(f"Users | Avatar | Tarafından : {ctx.author}")

    @commands.guild_only()
    @commands.command(name="Sunucu", brief = "Server bilgilerini getirir.",aliases = ['sunucu','server','Server'])
    async def server_command(self,ctx):
        """Server Info
        Use of : server
        """
        member_count = len([m for m in ctx.guild.members if not m.bot])
        ServerE = discord.Embed(colour=0xffd500, timestamp=ctx.message.created_at)
        ServerE.set_author(name=ctx.message.guild.name,icon_url=ctx.guild.icon_url)
        ServerE.set_thumbnail(url=ctx.guild.icon_url)
        ServerE.add_field(name="Sahibi", value=f"`{ctx.guild.owner}`")
        ServerE.add_field(name="Açılış Tarihi", value=ctx.guild.created_at.strftime("`%#d/%m/%Y`"))
        ServerE.add_field(name="Bölge", value=f"`{ctx.guild.region}`")
        ServerE.add_field(name="Kanal Sayıları", value=f"Metin: `{len(ctx.guild.text_channels)}`\nSes: `{len(ctx.guild.voice_channels)}`\nKategori: `{len(ctx.guild.categories)}`")
        ServerE.add_field(name="Üye Sayıları", value=f"İnsan: `{member_count}`\nBot: `{len(ctx.guild.members)-member_count}`")
        ServerE.add_field(name="Rol Sayısı", value=f"`{len(ctx.guild.roles)}`")
        ServerE.add_field(name="Takviye Seviyesi", value=f"`{ctx.guild.premium_tier}`")
        ServerE.add_field(name="Takviye Sayısı", value=f"`{ctx.guild.premium_subscription_count}`")
        ServerE.set_footer(text=f"Sunucu ID:{ctx.guild.id}")
        
        await ctx.send(embed=ServerE)
        
        logger.info(f"Users | Sunucu Bilgileri : {ctx.guild.name} | Tarafından : {ctx.author}")

def setup(client):
    client.add_cog(Users(client))