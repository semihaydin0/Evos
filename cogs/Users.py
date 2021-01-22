#MIT License
#Copyright (c) 2020 Semih Aydın
#UTF-8

import discord
from discord.ext import commands
from PIL import Image,ImageFont,ImageDraw
import io
import os
from logging_files.users_log import logger

class Users(commands.Cog):
    def __init__(self,client):
        self.client = client

    @commands.guild_only()
    @commands.command(name="Profil", brief = "Kullanıcının profil bilgilerini görüntüler.",aliases = ['profil','Profile','profile'])
    async def profile_command(self,ctx,member : discord.Member = None):
        """Profile
        Use of : profil
        """
        if member is None :
            member = ctx.author
        
        profileImg = Image.open("./images/info-background.jpg")
        draw = ImageDraw.Draw(profileImg)
        defaultSize = 80
        
        if  len(str(member)) > 25 or len(str(ctx.author)) > 25 or len(str(member.top_role)) > 25 :
            defaultSize -= max(len(str(member)),len(str(ctx.author)),len(str(member.top_role)))-5
        
        defaultFont = ImageFont.truetype("./assets/fonts/Oxanium-Regular.ttf", defaultSize)
        headerFont = ImageFont.truetype("./assets/fonts/SansitaSwashed-VariableFont_wght.ttf", 150)
        
        draw.text((500, 15), "Profil Bilgileri", (255, 255, 255), font=headerFont)
        draw.text((50, 264), f"Kullanıcı Adı: {member}", (255, 255, 255), font=defaultFont)
        draw.text((50, 364), "Kayıt Tarihi: {}".format(member.created_at.strftime("%#d/%m/%Y")), (255, 255, 255), font=defaultFont)
        draw.text((50, 464), "Katılma Tarihi: {}".format(member.joined_at.strftime("%#d/%m/%Y")), (255, 255, 255), font=defaultFont)
        draw.text((50, 564), f"En Yüksek Rolü: {member.top_role}", (255, 255, 255), font=defaultFont)
        draw.text((50, 664), f"ID: {member.id}", (255, 255, 255), font=defaultFont)
        draw.text((190, 868), f"Tarafından: {ctx.author}", (255, 255, 255), font=defaultFont)
        
        author_avatar_asset = ctx.author.avatar_url_as(format='jpg', size=128)
        member_avatar_asset = member.avatar_url_as(format='jpg', size=512)
        
        author_buffer_avatar = io.BytesIO(await author_avatar_asset.read())
        member_buffer_avatar = io.BytesIO(await member_avatar_asset.read())
        
        author_image = Image.open(author_buffer_avatar)
        author_image = author_image.resize((128, 128))
        
        member_image = Image.open(member_buffer_avatar)
        member_image = member_image.resize((512, 512))
        
        circle_image = Image.new('L', (128, 128))
        circle_draw = ImageDraw.Draw(circle_image)
        circle_draw.ellipse((0, 0, 128, 128), fill=255)

        circle_image_2 = Image.new('L', (512, 512))
        circle_draw_2 = ImageDraw.Draw(circle_image_2)
        circle_draw_2.ellipse((0, 0, 512, 512), fill=255)
        
        profileImg.paste(author_image, (50, 835), circle_image)
        profileImg.paste(member_image, (1360, 245), circle_image_2)
        profileImg.save("profile.png")

        await ctx.send(file=discord.File("profile.png"))
        
        os.remove("profile.png")
        
        logger.info(f"Users | Profil | Tarafından : {ctx.author}")
    
    @commands.command(name="Avatar",brief = "Kullanıcının avatarını görüntüler.",aliases = ['avatar'])
    async def avatar_command(self,ctx,member : discord.Member=None):
        """Avatar
        Use of : avatar
        """
        if member is None : 
            member = ctx.message.author
        avatarEmbed = discord.Embed(colour=member.color)
        avatarEmbed.set_author(name = member)
        avatarEmbed.set_image(url = f'{member.avatar_url}')
        
        await ctx.send(embed=avatarEmbed)
        
        logger.info(f"Users | Avatar | Tarafından : {ctx.author}")

    @commands.guild_only()
    @commands.command(name="Sunucu", brief = "Server bilgilerini görüntüler.",aliases = ['sunucu','server','Server'])
    async def server_command(self,ctx):
        """Server Info
        Use of : server
        """
        serverImg = Image.open("./images/info-background.jpg")
        draw = ImageDraw.Draw(serverImg)
        defaultSize = 70
        
        if  len(str(ctx.guild.owner)) > 25 :
            defaultSize -= len(str(ctx.guild.owner)) - 10

        defaultFont = ImageFont.truetype("./assets/fonts/Oxanium-Regular.ttf", defaultSize)
        headerFont = ImageFont.truetype("./assets/fonts/SansitaSwashed-VariableFont_wght.ttf", 150)

        draw.text((475, 15), "Sunucu Bilgileri", (255, 255, 255), font=headerFont)
        draw.text((50, 264), f"Sahibi\n{ctx.guild.owner}", (255, 255, 255), font=defaultFont)
        draw.text((775, 264), "Açılış Tarihi\n{}".format(ctx.guild.created_at.strftime("%#d/%m/%Y")), (255, 255, 255), font=defaultFont)
        draw.text((1475, 264), f"Bölge\n{ctx.guild.region}", (255, 255, 255), font=defaultFont)
        draw.text((50, 475), f"Kanal Sayıları\nMetin: {len(ctx.guild.text_channels)}\nSes: {len(ctx.guild.voice_channels)}\nKategori: {len(ctx.guild.categories)}", (255, 255, 255), font=defaultFont)
        draw.text((775, 475), f"Üye Sayıları\nİnsan: {len([m for m in ctx.guild.members if not m.bot])}\nBot: {len([m for m in ctx.guild.members if m.bot])}", (255, 255, 255), font=defaultFont)
        draw.text((1475, 475), f"Rol Sayısı\n{len(ctx.guild.roles)}", (255, 255, 255), font=defaultFont)
        draw.text((50, 810), f"Takviye Seviyesi\n{ctx.guild.premium_tier}", (255, 255, 255), font=defaultFont)
        draw.text((775, 810), f"Takviye Sayısı\n{ctx.guild.premium_subscription_count}", (255, 255, 255), font=defaultFont)
        
        guild_avatar_asset = ctx.guild.icon_url_as(format='jpg', size=512)
        guild_buffer_avatar = io.BytesIO(await guild_avatar_asset.read())

        guild_image = Image.open(guild_buffer_avatar)
        guild_image = guild_image.resize((512, 512))

        circle_image = Image.new('L', (512, 512))
        circle_draw = ImageDraw.Draw(circle_image)
        circle_draw.ellipse((0, 0, 512, 512), fill=255)

        serverImg.paste(guild_image, (1430, 580), circle_image)
        serverImg.save("server.png")

        await ctx.send(file=discord.File("server.png"))

        os.remove("server.png")

        logger.info(f"Users | Sunucu : {ctx.guild.name} | Tarafından : {ctx.author}")

def setup(client):
    client.add_cog(Users(client))