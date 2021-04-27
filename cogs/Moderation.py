#MIT License
#Copyright (c) 2020 Semih Aydın
#UTF-8

import discord
from discord.ext import commands
import sqlite3
from logging_files.moderation_log import logger

class Moderation(commands.Cog):
    def __init__(self,client):
        self.client = client

    @commands.guild_only()
    @commands.has_permissions(manage_messages=True)
    @commands.bot_has_permissions(manage_messages=True)
    @commands.cooldown(1, 10, commands.BucketType.guild)
    @commands.command(name= "Sil", brief = "Metin kanalından mesaj siler.",aliases=['sil','Purge','purge'])
    async def purge_command(self,ctx,amount: int):
        if amount <= 100 :
            cleaned = await ctx.message.channel.purge(limit=amount + 1)
            purgeEmbed=discord.Embed(title=f"Bu kanaldan {len(cleaned)-1} mesaj silindi.",colour=0xffd500)
            purgeEmbed.set_footer(text=f"Tarafından: {ctx.author}", icon_url=ctx.author.avatar_url)

            await ctx.send(embed=purgeEmbed, delete_after=3)

            logger.info(f"Moderation | Purge | Tarafından: {ctx.author}")
        else:
            purgeEmbed_2=discord.Embed(title="Hata",description="Tek seferde 100'den fazla mesaj silemezsiniz.",colour=0xd92929)

            await ctx.send(embed = purgeEmbed_2)

    @commands.guild_only()
    @commands.has_permissions(kick_members=True)
    @commands.bot_has_permissions(kick_members=True)
    @commands.command(name = "At",brief = "Sunucudan üye atar.",aliases=['at','Kick','kick'])
    async def kick_command(self,ctx,member: discord.Member, *,reason: str=None):
        if member != ctx.author :

            if reason==None :
                reason = "Belirtilmemiş"

            await member.kick(reason=reason)
            file = discord.File("./images/kick.gif", filename="kick.gif")

            kickEmbed=discord.Embed(title=f"{member} sunucudan atıldı!",description=f"Sebep: {reason}",colour=0xffd500,timestamp=ctx.message.created_at)
            kickEmbed.set_image(url="attachment://kick.gif")
            kickEmbed.set_footer(text=f"Tarafından: {ctx.author}",icon_url=ctx.author.avatar_url)

            await ctx.send(file=file,embed=kickEmbed)

            logger.info(f"Moderation | Kick | Tarafından: {ctx.author}")
        else :
            kickEmbed_2=discord.Embed(title="Hata",description="Hatalı argüman kullanımı.",colour=0xd92929)

            await ctx.send(embed = kickEmbed_2)

    @commands.guild_only()
    @commands.has_permissions(ban_members=True)
    @commands.bot_has_permissions(ban_members=True)
    @commands.command(name="Yasakla" ,brief = "Sunucudan üye yasaklar.",aliases=['yasakla','Ban','ban'])
    async def ban_command(self,ctx,member: discord.Member, *,reason: str=None):
        if member != ctx.author :

            if reason == None :
                reason = "Belirtilmemiş"

            await member.ban(reason=reason)
            file = discord.File("./images/banned.gif", filename="banned.gif")

            banEmbed=discord.Embed(title=f"{member} sunucudan yasaklandı!",description=f"Sebep: {reason}",colour=0xffd500,timestamp=ctx.message.created_at)
            banEmbed.set_image(url="attachment://banned.gif")
            banEmbed.set_footer(text=f"Tarafından: {ctx.author}",icon_url=ctx.author.avatar_url)

            await ctx.send(file=file,embed=banEmbed)

            logger.info(f"Moderation | Ban | Tarafından: {ctx.author}")
        else :
            banEmbed_2=discord.Embed(title="Hata",description="Hatalı argüman kullanımı.",colour=0xd92929)

            await ctx.send(embed = banEmbed_2)

    @commands.guild_only()
    @commands.has_permissions(ban_members=True)
    @commands.bot_has_permissions(ban_members=True)
    @commands.command(name ="Unban",brief = "Yasaklanan üyenin yasağını kaldırır.",aliases=["unban"])
    async def unban_command(self,ctx,member: str):
        control = 0

        for i in range(len(member)) :

            if "#" in member[i] :
                control = 1

        if control != 0 :
            status = False
            banned_user = await ctx.guild.bans()
            member_name, member_discriminator = member.split('#')

            for ban_entry in banned_user :
                user = ban_entry.user

                if (user.name,user.discriminator) == (member_name,member_discriminator) :

                    await ctx.guild.unban(user)
                    unbanEmbed=discord.Embed(title=f"{user} adlı kullanıcının yasaklanması kaldırıldı!",colour=0xffd500,timestamp=ctx.message.created_at)
                    unbanEmbed.set_footer(text=f"Tarafından: {ctx.author}",icon_url=ctx.author.avatar_url)

                    await ctx.send(embed=unbanEmbed)
                    status = True

                    logger.info(f"Moderation | Unban | Tarafından: {ctx.author}")

            if status == False :
                unbanEmbed_2=discord.Embed(title="Hata",description="Belirtilen kullanıcı yasaklananlar listesinde bulunamadı.",colour=0xd92929)

                await ctx.send(embed=unbanEmbed_2)
        else :
            unbanEmbed_3=discord.Embed(title="Hata",description="Üyenin tam adını giriniz.",colour=0xd92929)

            await ctx.send(embed = unbanEmbed_3)

    @commands.guild_only()
    @commands.has_permissions(manage_roles=True)
    @commands.bot_has_permissions(manage_roles=True)
    @commands.command(name="Sustur", brief = "Üyeyi belirlediğiniz süreye kadar susturur.",aliases=["sustur","mute"])
    async def mute_command(self,ctx,member: discord.Member, minute: int):
        role = discord.utils.get(ctx.guild.roles,name = "Muted")

        if member != ctx.author :

            if role in member.roles :
                muteEmbed=discord.Embed(title="Hata",description="Belirtilen kullanıcı zaten susturulmuş.",colour=0xd92929)

                await ctx.send(embed=muteEmbed)

            else :

                if role == None :
                    role = await ctx.guild.create_role(name="Muted")

                    for channel in ctx.guild.channels:
                        await channel.set_permissions(role,send_messages = False,speak = False)

                try :

                    if minute > 0 :

                            await member.add_roles(role)
                            db = sqlite3.connect('data/server/Mute.db')
                            cursor = db.cursor()

                            try :
                                cursor.execute("INSERT INTO MutedUsers VALUES (?,?)",(str(member.id),minute,))
                                db.commit()
                            except Exception as e:
                                await ctx.send(":thinking: Görünüşe göre şu anda susturulmuş kullanıcı kayıtlarına ulaşamıyoruz. Belirtilen kullanıcı susturuldu ancak yasağını manuel kaldırman gerekir.")

                                logger.error(f"Moderation | Mute | Error: {e}")
                                return
                            finally :
                                cursor.close()
                                db.close()

                            muteEmbed_2=discord.Embed(title=f"{member} {minute} dakika susturuldu !",colour=0xffd500,timestamp=ctx.message.created_at)
                            muteEmbed_2.set_footer(text=f"Tarafından: {ctx.author}",icon_url=ctx.author.avatar_url)

                            await ctx.send(embed=muteEmbed_2)

                            logger.info(f"Moderation | Mute | Tarafından: {ctx.author}")
                    else :
                        await member.add_roles(role)

                        muteEmbed_3=discord.Embed(title=f"{member} süresiz susturuldu !",colour=0xffd500,timestamp=ctx.message.created_at)
                        muteEmbed_3.set_footer(text=f"Tarafından: {ctx.author}",icon_url=ctx.author.avatar_url)

                        await ctx.send(embed=muteEmbed_3)
                except Exception:
                    muteEmbed_4=discord.Embed(title="Hata",description=f"Bu işlem için Muted rolünün kademesi {self.client.user.name} rolünden en az 1 kademe altında olması gerekir.",colour=0xd92929)

                    await ctx.send(embed = muteEmbed_4)
        else :
            muteEmbed_5=discord.Embed(title="Hata",description="Hatalı argüman kullanımı.",colour=0xd92929)

            await ctx.send(embed=muteEmbed_5)

    @commands.guild_only()
    @commands.has_permissions(manage_roles=True)
    @commands.bot_has_permissions(manage_roles=True)
    @commands.command(name = "Unmute",brief = "Üyenin konuşma yasağını kaldırır.",aliases=["unmute"])
    async def unmute_command(self,ctx,member: discord.Member):
        role = discord.utils.get(ctx.guild.roles,name = "Muted")

        if role != None :

            if role in member.roles:

                    db = sqlite3.connect('data/server/Mute.db')
                    cursor = db.cursor()

                    try :
                        cursor.execute("DELETE FROM MutedUsers WHERE USER_ID=?",(str(member.id),))
                        db.commit()
                    except Exception as e:
                        await ctx.send(":thinking: Görünüşe göre şu anda susturulmuş kullanıcı kayıtlarına ulaşamıyoruz.Daha sonra tekrar deneyebilirsin.")

                        logger.error(f"Moderation | Unmute | Error: {e}")
                        return
                    finally :
                        cursor.close()
                        db.close()

                    try :
                        await member.remove_roles(role)
                    except Exception:
                        unmuteEmbed_2=discord.Embed(title="Hata",description=f"Bu işlem için Muted rolünün kademesi {self.client.user.name} rolünden en az 1 kademe altında olması gerekir.",colour=0xd92929)

                        await ctx.send(embed = unmuteEmbed_2)
                        return

                    unmuteEmbed=discord.Embed(title=f"{member} adlı kullanıcının susturulma cezası kaldırıldı!",colour=0xffd500,timestamp=ctx.message.created_at)
                    unmuteEmbed.set_footer(text=f"Tarafından: {ctx.author}",icon_url=ctx.author.avatar_url)

                    await ctx.send(embed=unmuteEmbed)

                    logger.info(f"Moderation | Unmute | Tarafından: {ctx.author}")
            else :
                unmuteEmbed_3=discord.Embed(title="Hata",description=f"{member} adlı kullanıcının susturma cezası bulunamadı.",colour=0xd92929)

                await ctx.send(embed=unmuteEmbed_3)
        else :
            unmuteEmbed_4=discord.Embed(title="Hata",description="Daha önceden kimse susturulmamış ya da rol silinmiş olabilir.",colour=0xd92929)

            await ctx.send(embed=unmuteEmbed_4)

    @commands.guild_only()
    @commands.has_permissions(change_nickname=True)
    @commands.bot_has_permissions(change_nickname=True)
    @commands.command(name="Rename" ,brief = "Üyenin sunucu içindeki takma adını değiştirir.",aliases=["rename"])
    async def rename_command(self,ctx,member : discord.Member,nick: str):
        if member != ctx.author :
            await member.edit(nick=nick)

            renameEmbed=discord.Embed(title=f"{member} adlı kullanıcının ismi değiştirildi.",colour=0xffd500,timestamp=ctx.message.created_at)
            renameEmbed.set_footer(text=f"Tarafından: {ctx.author}",icon_url=ctx.author.avatar_url)

            await ctx.send(embed=renameEmbed)

            logger.info(f"Moderation | Rename | Tarafından: {ctx.author}")
        else :
            renameEmbed_2=discord.Embed(title="Hata",description="Hatalı argüman kullanımı.",colour=0xd92929)

            await ctx.send(embed=renameEmbed_2)

def setup(client):
    client.add_cog(Moderation(client))