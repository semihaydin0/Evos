#MIT License
#Copyright (c) 2020 Semih Aydın
#UTF-8

import discord
from discord.ext import commands
from PIL import Image,ImageFont,ImageDraw
import sqlite3
import asyncio
import io
import os
from logging_files.guild_log import logger
from Evos import get_version_number

class InvalidLoggingValue(commands.CommandError):
    pass

class AlreadyHasALogChannel(commands.CommandError):
    pass

class NoLogChannel(commands.CommandError):
    pass

def check_channel(author,channel):
    def inner_check(message):
        return len(message.channel_mentions) == 1 and message.author == author and message.channel.id == channel

    return inner_check

def check_autorole(author,channel):
    def inner_check(message):
        return len(message.role_mentions) == 1 and message.author == author and message.channel.id == channel

    return inner_check

def check_prefix(author,channel):
    def inner_check(message):
        return len(message.content) <= 3 and message.author == author and message.channel.id == channel

    return inner_check

def check_message(author,channel):
    def inner_check(message):
        return message.author == author and message.channel.id == channel

    return inner_check

class Guild(commands.Cog):
    def __init__(self,client):
        self.client = client

    @commands.command(name = "Wlmessage",brief = "Yeni gelen üyeler için karşılama mesajı gönderir.",aliases = ["wlmessage"])
    @commands.has_permissions(administrator=True)
    async def member_welcome_command(self,ctx):
        await ctx.send(f"Selam {ctx.author.mention}!\nSeçmek istediğin kanalı belirleyelim.\n`Belirlemek istediğin kanalı etiketlemen yeterli.`")

        try:
            channelSelection = await self.client.wait_for('message',check = check_channel(ctx.author,ctx.message.channel.id) ,timeout=30)
        except asyncio.TimeoutError:
            await ctx.send(f":sleeping: {ctx.author.mention} Belirlenen sürede senden herhangi bir yanıt alamadık.")

        else :
            db = sqlite3.connect('data/server/Data.db')
            cursor = db.cursor()
            try :
                channelID = channelSelection.channel_mentions[0].id
                cursor.execute("UPDATE ServerData SET WELCOME_CHANNEL_ID=? WHERE SERVER_ID=?",(channelID,ctx.author.guild.id,))
                db.commit()

                await ctx.send(f"Harika! :partying_face: Artık {channelSelection.channel_mentions[0].mention} kanalında yeni üyeler için bilgilendirme mesajı gönderilecek.")

                logger.info(f"Guild | Wlmessage | Sunucu : {ctx.guild.name} | Tarafından : {ctx.author}")
            except Exception as e:
                await ctx.send(":thinking: Görünüşe göre şu anda sunucu kayıtlarına ulaşamıyoruz.Daha sonra tekrar deneyebilirsin.")

                logger.error(f"Guild | Wlmessage | Error: {e}")
            finally :
                cursor.close()
                db.close()

    @commands.command(name = "Lvmessage",brief = "Ayrılan üyeler için bilgilendirme mesajı gönderir.",aliases = ["lvmessage"])
    @commands.has_permissions(administrator=True)
    async def member_leave_command(self,ctx):
        await ctx.send(f"Selam {ctx.author.mention}!\nSeçmek istediğin kanalı belirleyelim.\n`Belirlemek istediğin kanalı etiketlemen yeterli.`")

        try:
            channelSelection = await self.client.wait_for('message',check = check_channel(ctx.author,ctx.message.channel.id) ,timeout=30)
        except asyncio.TimeoutError:
            await ctx.send(f":sleeping: {ctx.author.mention} Belirlenen sürede senden herhangi bir yanıt alamadık.")

        else :
            db = sqlite3.connect('data/server/Data.db')
            cursor = db.cursor()
            try :
                channelID = channelSelection.channel_mentions[0].id
                cursor.execute("UPDATE ServerData SET LEAVE_CHANNEL_ID=? WHERE SERVER_ID=?",(channelID,ctx.author.guild.id,))
                db.commit()

                await ctx.send(f"Harika! :partying_face: Artık {channelSelection.channel_mentions[0].mention} kanalında ayrılan üyeler için bilgilendirme mesajı gönderilecek.")

                logger.info(f"Guild | Lvmessage | Sunucu : {ctx.guild.name} | Tarafından : {ctx.author}")
            except Exception as e:
                await ctx.send(":thinking: Görünüşe göre şu anda sunucu kayıtlarına ulaşamıyoruz.Daha sonra tekrar deneyebilirsin.")

                logger.error(f"Guild | Lvmessage | Error: {e}")
            finally :
                cursor.close()
                db.close()

    @commands.command(name = "Setautorole",brief = "Yeni gelen üyeler için otomatik rol verir.",aliases = ["setautorole"])
    @commands.has_permissions(administrator=True)
    async def autorole_command(self,ctx):
        await ctx.send(f"Selam {ctx.author.mention}!\nSeçmek istediğin rolü belirleyelim.\n`Belirlemek istediğin rolü etiketlemen yeterli.`")

        try:
            roleSelection = await self.client.wait_for('message',check = check_autorole(ctx.author,ctx.message.channel.id) ,timeout=30)
        except asyncio.TimeoutError:
            await ctx.send(f":sleeping: {ctx.author.mention} Belirlenen sürede senden herhangi bir yanıt alamadık.")

        else :
            db = sqlite3.connect('data/server/Data.db')
            cursor = db.cursor()
            try :
                roleID = roleSelection.role_mentions[0].id
                cursor.execute("UPDATE ServerData SET AUTOROLE_ID=? WHERE SERVER_ID=?",(roleID,ctx.author.guild.id,))
                db.commit()

                await ctx.send(f"Harika! :partying_face: Artık yeni gelen üyelere {roleSelection.role_mentions[0].mention} rolü verilecek.\n`Uyarı: Evos'un bu işlevi tam olarak yerine getirebilmesi için roller kısmından Evos'un rolünü {roleSelection.role_mentions[0]} rolünden en az 1 kademe üstüne taşıman gerekli.`")

                logger.info(f"Guild | Autorole | Sunucu : {ctx.guild.name} | Tarafından : {ctx.author}")
            except Exception as e:
                await ctx.send(":thinking: Görünüşe göre şu anda sunucu kayıtlarına ulaşamıyoruz.Daha sonra tekrar deneyebilirsin.")

                logger.error(f"Guild | Autorole | Error: {e}")
            finally :
                cursor.close()
                db.close()

    @commands.command(name = "ChangePrefix",brief = "Evos'un komut ön ekini değiştirir.",aliases = ["changeprefix"])
    @commands.has_permissions(administrator=True)
    async def change_prefix_command(self,ctx):
        await ctx.send(f"Selam {ctx.author.mention}!\nSeçmek istediğin komut ön ekini belirleyelim.\n`Maksimum 3 karakter olmasını ve son karakterinde işaret bulundurmanızı öneriyoruz.`")

        try:
            prefixSelection = await self.client.wait_for('message',check = check_prefix(ctx.author,ctx.message.channel.id) ,timeout=60)
        except asyncio.TimeoutError:
            await ctx.send(f":sleeping: {ctx.author.mention} Belirlenen sürede senden herhangi bir yanıt alamadık.")

        else :
            db = sqlite3.connect('data/server/Data.db')
            cursor = db.cursor()
            try :
                cursor.execute("UPDATE ServerData SET CUSTOM_PREFIX=? WHERE SERVER_ID=?",(str(prefixSelection.content),ctx.author.guild.id,))
                db.commit()

                await ctx.send(f"Harika! :partying_face: Bu sunucu için komut ön eki **{prefixSelection.content}** olarak ayarlandı.")

                logger.info(f"Guild | Prefix | Sunucu : {ctx.guild.name} | Tarafından : {ctx.author}")
            except Exception as e:
                await ctx.send(":thinking: Görünüşe göre şu anda sunucu kayıtlarına ulaşamıyoruz.Daha sonra tekrar deneyebilirsin.")

                logger.error(f"Guild | ChangePrefix | Error: {e}")

    @commands.command(name = "ResetConfig",brief = "Sunucu ayarlarını sıfırlar.",aliases = ["resetconfig"])
    @commands.has_permissions(administrator=True)
    async def server_config_reset_command(self,ctx):
        db = sqlite3.connect('data/server/Data.db')
        cursor = db.cursor()
        db2 = sqlite3.connect('data/server/Config.db')
        cursor2 = db2.cursor()

        try :
            cursor.execute("UPDATE ServerData SET CUSTOM_PREFIX = '.',AUTOROLE_ID = NULL,WELCOME_CHANNEL_ID = NULL,LEAVE_CHANNEL_ID = NULL WHERE SERVER_ID = ?",(str(ctx.author.guild.id),))
            db.commit()
            cursor.close()
            db.close()

            cursor2.execute("DELETE FROM AutoMessage WHERE SERVER_ID = ?",(str(ctx.author.guild.id),))
            db2.commit()

            await ctx.send("Harika! :partying_face: Bu sunucunun tüm ayarları sıfırlandı. Prefix(komut ön eki) varsayılan **.(nokta)** olarak ayarlandı.")
        except Exception as e:
            await ctx.send(":thinking: Görünüşe göre şu anda sunucu kayıtlarına ulaşamıyoruz.Daha sonra tekrar deneyebilirsin.")

            logger.error(f"Guild | ResetServerConfig | Error: {e}")
        finally :
            cursor2.close()
            db2.close()

    @commands.command(name = "Automessage",brief = "İstediğiniz kanala otomatik mesaj gönderir.",aliases = ["automessage"])
    @commands.has_permissions(administrator=True)
    async def auto_message_scheduler_command(self,ctx):
        await ctx.send(f"Selam {ctx.author.mention}!\nÖnce istediğin duyurmak istediğin mesajı belirleyelim.\n`Mesajının maksimum 512 karakter olmasını öneriyoruz.`")

        try:
            messageSelection = await self.client.wait_for('message',check = check_message(ctx.author,ctx.message.channel.id) ,timeout=300)
        except asyncio.TimeoutError:
            await ctx.send(f":sleeping: {ctx.author.mention} Belirlenen sürede senden herhangi bir yanıt alamadık.")

        else :
            await ctx.send("Harika! :partying_face: Şimdi bu mesajın kaç saatte bir yayınlanmasını gerektiğini belirleyelim.\n`Sadece tam sayı girişi yapman gerekir. Aksi taktirde bu sistem çalışmayacaktır.`")

            try:
                timeSelection = await self.client.wait_for('message',check = check_message(ctx.author,ctx.message.channel.id) ,timeout=30)
            except asyncio.TimeoutError:
                await ctx.send(f":sleeping: {ctx.author.mention} Belirlenen sürede senden herhangi bir yanıt alamadık.")

            else :
                db = sqlite3.connect('data/server/Config.db')
                cursor = db.cursor()
                try :
                    cursor.execute("INSERT INTO AutoMessage VALUES (?,?,?,?,?)",(str(ctx.message.guild.id),str(ctx.message.channel.id),str(messageSelection.content),int(timeSelection.content),int(timeSelection.content)))
                    db.commit()

                    await ctx.send(f"Harika! :partying_face: Artık bu kanalda her **{timeSelection.content}** saatte bir mesajın yayınlanacak.")

                    logger.info(f"Guild | AutoMessage | Tarafından: {ctx.author}")
                except Exception as e:
                    await ctx.send(":thinking: Görünüşe göre şu anda sunucu kayıtlarına ulaşamıyoruz.Daha sonra tekrar deneyebilirsin.")

                    logger.error(f"Guild | AutoMessage | Error: {e}")
                finally :
                    cursor.close()
                    db.close()

    @commands.command(name = "Logging",brief = "Sunucunuz için log ayarının açılmasını/kapatılmasını sağlar.",aliases = ["logging"])
    @commands.has_permissions(administrator=True)
    async def logging_command(self, ctx, value: int):
        if value not in (0, 1):
            raise InvalidLoggingValue

        db = sqlite3.connect('data/server/Config.db')
        cursor = db.cursor()

        if value == 1:
            log_channel = discord.utils.get(ctx.guild.text_channels, name=f"{self.client.user.name}-log".lower())

            if log_channel is None:
                overwrites = {
                    ctx.guild.default_role: discord.PermissionOverwrite(read_messages=False),
                }
                channel = await ctx.guild.create_text_channel(f"{self.client.user.name}-log", overwrites=overwrites,position = 0,topic=f"{self.client.user.name} tarafından tutulan denetim kayıtları.")

                try :
                    cursor.execute("INSERT INTO Log VALUES (?,?)",(str(ctx.guild.id),str(channel.id)))
                    db.commit()

                    await ctx.send(f"Harika! :partying_face: Artık {channel.mention} kanalına sunucu ve üyeler ile ilgili değişiklikler gönderilecek.")
                except Exception as e:

                    logger.error(f"Guild | Data | Error: {e}")
                finally :
                    cursor.close()
                    db.close()
            else:
                raise AlreadyHasALogChannel

            logger.info(f"Guild | Logging-1 | Tarafından: {ctx.author}")
        else :
            try :
                cursor.execute("DELETE FROM Log WHERE SERVER_ID = ?",(str(ctx.guild.id),))
                db.commit()
            except Exception as e:

                logger.error(f"Guild | Data | Error: {e}")
            finally :
                cursor.close()
                db.close()

            status = 0

            for channel in ctx.guild.text_channels:
                if channel.name == f"{self.client.user.name}-log".lower():
                    await channel.delete()
                    status+=1

            if status == 0:
                raise NoLogChannel

            loggingEmbed = discord.Embed(title="Log kanalı silindi.",description="Aynı komut üzerinden tekrar aktifleştirebilirsin.",colour=0xffd500)

            await ctx.send(embed=loggingEmbed)

            logger.info(f"Guild | Logging-0 | Tarafından: {ctx.author}")

    @logging_command.error
    async def logging_command_error(self, ctx, exc):
        if isinstance(exc, InvalidLoggingValue):
            loggingEmbed_2=discord.Embed(title="Geçersiz bir değer girdiniz.",description="Sadece 1 (Açmak) ve 0 (Kapatmak) değerlerini girebilirsiniz.",colour=0xffd500)

            await ctx.send(embed=loggingEmbed_2)
        elif isinstance(exc, AlreadyHasALogChannel):
            loggingEmbed_3=discord.Embed(title="Halihazırda bir log kanalı var.",colour=0xffd500)

            await ctx.send(embed=loggingEmbed_3)
        elif isinstance(exc, NoLogChannel):
            loggingEmbed_4=discord.Embed(title="Log kanalı bulunamadı.",colour=0xffd500)

            await ctx.send(embed=loggingEmbed_4)

    @commands.Cog.listener()
    async def on_message_edit(self, before, after):
        if not after.author.bot:
            db = sqlite3.connect('data/server/Config.db')
            cursor = db.cursor()

            try :
                cursor.execute("SELECT CHANNEL_ID FROM Log WHERE SERVER_ID = ?",(str(after.author.guild.id),))
                data = cursor.fetchone()

                if data[0] != None :
                    channelID = data[0]
                    channel = discord.utils.get(after.author.guild.text_channels, id=int(channelID))

                if channel is not None:
                    messageEditEmbed = discord.Embed(title="Mesaj Güncellemesi",description="Düzenlenen Mesaj",colour=0x34ebe2)
                    messageEditEmbed.set_thumbnail(url=f'{after.author.avatar_url}')
                    messageEditEmbed.add_field(name="Önce",value=before.content,inline=False)
                    messageEditEmbed.add_field(name="Sonra",value=after.content,inline=False)
                    messageEditEmbed.set_footer(text=f"Üye: {after.author}")

                    await channel.send(embed=messageEditEmbed)
            except Exception as e:

                logger.error(f"Guild | Data | Error: {e}")
            finally :
                cursor.close()
                db.close()

    @commands.Cog.listener()
    async def on_message_delete(self, message):
        if not message.author.bot:
            db = sqlite3.connect('data/server/Config.db')
            cursor = db.cursor()

            try :
                cursor.execute("SELECT CHANNEL_ID FROM Log WHERE SERVER_ID = ?",(str(message.author.guild.id),))
                data = cursor.fetchone()

                if data[0] != None :
                    channelID = data[0]
                    channel = discord.utils.get(message.author.guild.text_channels, id=int(channelID))

                if channel is not None:
                    messageDeleteEmbed = discord.Embed(title="Mesaj Güncellemesi",description="Silinen Mesaj",colour=0x3459eb)
                    messageDeleteEmbed.set_thumbnail(url=f'{message.author.avatar_url}')
                    messageDeleteEmbed.add_field(name="Mesaj",value=message.content)
                    messageDeleteEmbed.set_footer(text=f"Üye: {message.author}")

                    await channel.send(embed=messageDeleteEmbed)
            except Exception as e:

                logger.error(f"Guild | Data | Error: {e}")
            finally :
                cursor.close()
                db.close()

    @commands.Cog.listener()
    async def on_guild_update(self, before, after):
        db = sqlite3.connect('data/server/Config.db')
        cursor = db.cursor()

        try :
            cursor.execute("SELECT CHANNEL_ID FROM Log WHERE SERVER_ID = ?",(str(before.id),))
            data = cursor.fetchone()

            if data[0] != None :
                channelID = data[0]
                channel = discord.utils.get(before.text_channels, id=int(channelID))

            if channel is not None:

                if before.name != after.name:
                    updatedNameEmbed = discord.Embed(title="Sunucu Güncellemesi",description="İsim Değişikliği",colour=0xa83832)
                    updatedNameEmbed.set_thumbnail(url=f'{before.icon_url}')
                    updatedNameEmbed.add_field(name="Önce",value=before.name,inline=False)
                    updatedNameEmbed.add_field(name="Sonra",value=after.name,inline=False)

                    await channel.send(embed=updatedNameEmbed)

                if before.region != after.region:
                    updatedRegionEmbed = discord.Embed(title="Sunucu Güncellemesi",description="Bölge Değişikliği",colour=0xa83832)
                    updatedRegionEmbed.set_thumbnail(url=f'{before.icon_url}')
                    updatedRegionEmbed.add_field(name="Önce",value=before.region,inline=False)
                    updatedRegionEmbed.add_field(name="Sonra",value=after.region,inline=False)

                    await channel.send(embed=updatedRegionEmbed)

                if before.owner != after.owner:
                    updatedOwnerEmbed = discord.Embed(title="Sunucu Güncellemesi",description="Sahiplik Değişikliği",colour=0xa83832)
                    updatedOwnerEmbed.set_thumbnail(url=f'{before.icon_url}')
                    updatedOwnerEmbed.add_field(name="Önce",value=before.owner,inline=False)
                    updatedOwnerEmbed.add_field(name="Sonra",value=after.owner,inline=False)

                    await channel.send(embed=updatedOwnerEmbed)

                if before.icon_url != after.icon_url:
                    updatedIconEmbed = discord.Embed(title="Sunucu Güncellemesi",description="Simge Değişikliği",colour=0xa83832)
                    updatedIconEmbed.set_image(url=after.icon_url)

                    await channel.send(embed=updatedIconEmbed)
        except Exception as e:

            logger.error(f"Guild | Data | Error: {e}")
        finally :
            cursor.close()
            db.close()

    @commands.Cog.listener()
    async def on_member_update(self, before, after):
        db = sqlite3.connect('data/server/Config.db')
        cursor = db.cursor()

        try :
            cursor.execute("SELECT CHANNEL_ID FROM Log WHERE SERVER_ID = ?",(str(before.guild.id),))
            data = cursor.fetchone()

            if data[0] != None :
                channelID = data[0]
                channel = discord.utils.get(before.guild.text_channels, id=int(channelID))

            if channel is not None:

                if before.display_name != after.display_name:
                    updatedNameEmbed = discord.Embed(title="Üye Güncellemesi",description="Kullanıcı Adı Değişikliği",colour=0x32a84a)
                    updatedNameEmbed.set_thumbnail(url=f'{before.avatar_url}')
                    updatedNameEmbed.add_field(name="Önce",value=before.display_name,inline=False)
                    updatedNameEmbed.add_field(name="Sonra",value=after.display_name,inline=False)
                    updatedNameEmbed.set_footer(text=f"Üye: {before}")

                    await channel.send(embed=updatedNameEmbed)

                if before.roles != after.roles:
                    updatedRolesEmbed = discord.Embed(title="Üye Güncellemesi",description="Rol Değişikliği",colour=0x32a84a)
                    updatedRolesEmbed.set_thumbnail(url=f'{before.avatar_url}')
                    updatedRolesEmbed.add_field(name="Önce",value=", ".join([r.mention for r in before.roles]),inline=False)
                    updatedRolesEmbed.add_field(name="Sonra",value=", ".join([r.mention for r in after.roles]),inline=False)
                    updatedRolesEmbed.set_footer(text=f"Üye: {before}")

                    await channel.send(embed=updatedRolesEmbed)
        except Exception as e:

            logger.error(f"Guild | Data | Error: {e}")
        finally :
            cursor.close()
            db.close()

    @commands.Cog.listener()
    async def on_member_join(self,member):
        db = sqlite3.connect('data/server/Data.db')
        cursor = db.cursor()

        try :
            cursor.execute("SELECT AUTOROLE_ID,WELCOME_CHANNEL_ID FROM ServerData WHERE SERVER_ID = ?",(member.guild.id,))
            data = cursor.fetchone()

            if data[0] != None :
                autoRoleID = data[0]
                autoRole = discord.utils.get(member.guild.roles, id=int(autoRoleID))

                if autoRole != None :
                    try :
                        await member.add_roles(autoRole)
                    except Exception as e:

                        logger.error(f"Guild | OnMemberJoin | Error: {e}")

            if data[1] is not None :
                channelID = data[1]
                channel = discord.utils.get(member.guild.text_channels, id=int(channelID))

                if channel != None :
                    welcomeImg = Image.open("./images/info-background.jpg")
                    draw = ImageDraw.Draw(welcomeImg)
                    W = 1920
                    defaultSize = 80
                    if len(member.guild.name)>50 :
                        defaultSize -= len(member.guild.name) - 25

                    headerFont = ImageFont.truetype("./assets/fonts/SansitaSwashed-VariableFont_wght.ttf", 150)
                    defaultFont = ImageFont.truetype("./assets/fonts/Oxanium-Regular.ttf", defaultSize)

                    headerMessage = "HOŞGELDİN"
                    countMemberMessage = f"{member.guild.name} | {len(member.guild.members)}.ÜYE"

                    w,h = draw.textsize(headerMessage,font=headerFont)
                    draw.text(((W-w)/2,h-141), headerMessage, (255, 255, 255), font=headerFont)
                    w,h = draw.textsize(countMemberMessage,font=defaultFont)
                    draw.text(((W-w)/2,900), countMemberMessage, (255, 255, 255), font=defaultFont)

                    member_avatar_asset = member.avatar_url_as(format='jpg', size=512)
                    member_buffer_avatar = io.BytesIO(await member_avatar_asset.read())

                    member_image = Image.open(member_buffer_avatar)
                    member_image = member_image.resize((512, 512))

                    circle_image = Image.new('L', (512, 512))
                    circle_draw = ImageDraw.Draw(circle_image)
                    circle_draw.ellipse((0, 0, 512, 512), fill=255)

                    welcomeImg.paste(member_image, (704, 300), circle_image)
                    welcomeImg.save(f"{member.id}.png")

                    await channel.send(f"Hoşgeldin, {member.mention}!",file=discord.File(f"{member.id}.png"))

                    os.remove(f"{member.id}.png")
        except Exception as e:

            logger.error(f"Guild | Data | Error: {e}")
        finally :
            cursor.close()
            db.close()

    @commands.Cog.listener()
    async def on_member_remove(self,member):
        db = sqlite3.connect('data/server/Data.db')
        cursor = db.cursor()

        if member.name != self.client.user.name :

            try :
                cursor.execute("SELECT LEAVE_CHANNEL_ID FROM ServerData WHERE SERVER_ID = ?",(member.guild.id,))
                data = cursor.fetchone()

                if data[0] != None :
                    channelID = data[0]
                    channel = discord.utils.get(member.guild.text_channels, id=int(channelID))

                    if channel != None :
                        leaveImg = Image.open("./images/info-background.jpg")
                        draw = ImageDraw.Draw(leaveImg)
                        W = 1920
                        defaultSize = 80
                        if len(member.guild.name)>50 :
                            defaultSize -= len(member.guild.name) - 25

                        headerFont = ImageFont.truetype("./assets/fonts/SansitaSwashed-VariableFont_wght.ttf", 150)
                        defaultFont = ImageFont.truetype("./assets/fonts/Oxanium-Regular.ttf", defaultSize)

                        headerMessage = "GÜLE GÜLE"
                        countMemberMessage = f"{member.guild.name} | {len(member.guild.members)} ÜYE"

                        w,h = draw.textsize(headerMessage,font=headerFont)
                        draw.text(((W-w)/2,h-133), headerMessage, (255, 255, 255), font=headerFont)
                        w,h = draw.textsize(countMemberMessage,font=defaultFont)
                        draw.text(((W-w)/2,900), countMemberMessage, (255, 255, 255), font=defaultFont)

                        member_avatar_asset = member.avatar_url_as(format='jpg', size=512)
                        member_buffer_avatar = io.BytesIO(await member_avatar_asset.read())

                        member_image = Image.open(member_buffer_avatar)
                        member_image = member_image.resize((512, 512))

                        circle_image = Image.new('L', (512, 512))
                        circle_draw = ImageDraw.Draw(circle_image)
                        circle_draw.ellipse((0, 0, 512, 512), fill=255)

                        leaveImg.paste(member_image, (704, 300), circle_image)
                        leaveImg.save(f"{member.id}.png")

                        await channel.send(f"{member.mention}, aramızdan ayrıldı!",file=discord.File(f"{member.id}.png"))

                        os.remove(f"{member.id}.png")
            except Exception as e:

                logger.error(f"Guild | Data | Error: {e}")
            finally :
                cursor.close()
                db.close()

    @commands.Cog.listener()
    async def on_guild_join(self, guild):
        db = sqlite3.connect('data/server/Data.db')
        cursor = db.cursor()

        try :
            cursor.execute("DELETE FROM ServerData WHERE SERVER_ID = ?",(str(guild.id),))
            cursor.execute("INSERT INTO ServerData VALUES (?,?,?,?,?)",(str(guild.id),'.','NULL','NULL','NULL'))
            db.commit()

            infoEmbed = discord.Embed(title = f"{self.client.user.name} burada! :hand_splayed:",colour=0x36393F)
            infoEmbed.add_field(name="Prefix",value="Varsayılan: **.** (Özelleştirilebilir)",inline=False)
            infoEmbed.add_field(name="Komut Listesi",value="Komut listesi için **yardım** komutunu kullanabilirsin.",inline=False)
            infoEmbed.add_field(name="Geliştirici misin ?",value="[Buradan](https://github.com/semihaydin0/Evos) kaynak kodlarını inceleyebilirsin.",inline=False)
            infoEmbed.set_footer(text=f"Mevcut Sürüm: v{get_version_number()} | PHOENIX#7103 tarafından 💖 ile geliştirildi!",icon_url=guild.icon_url)
            file = discord.File("images/evos.png", filename="evos.png")
            infoEmbed.set_thumbnail(url="attachment://evos.png")

            try :
                await guild.text_channels[0].send(file=file,embed=infoEmbed)
            except Exception as e:

                logger.error(f"Guild | OnGuildJoin | Error: {e}")
        except Exception as e:

            logger.error(f"Guild | Data | Error: {e}")
        finally :
            cursor.close()
            db.close()

def setup(client):
    client.add_cog(Guild(client))