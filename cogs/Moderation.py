import discord
from discord.utils import get
from discord.ext import commands

from logging_files.moderation_log import logger

class Moderation(commands.Cog):
    def __init__(self,client):
        self.client = client
    
    @commands.guild_only()
    @commands.has_permissions(manage_messages=True)
    @commands.bot_has_permissions(manage_messages=True)
    @commands.command(pass_context=True ,name= "Sil", brief = "Metin kanalından mesaj siler.",aliases=["sil","purge"])
    async def purge_command(self,ctx,amount : int):
          channel = ctx.message.channel
          cleaned = await channel.purge(limit=amount + 1)
          purge_embed=discord.Embed(title=f"Bu kanaldan {len(cleaned)-1} mesaj silindi.",colour=0xffd500)
          purge_embed.set_footer(text=f"Talep sahibi : {ctx.author.display_name}", icon_url=ctx.author.avatar_url)
          await ctx.send(embed=purge_embed, delete_after=5.0)
          logger.info(f"Moderation | Mesaj Silme : {len(cleaned)-1}  | Tarafından : {ctx.author}")

    @commands.guild_only()
    @commands.has_permissions(kick_members=True)
    @commands.bot_has_permissions(kick_members=True)
    @commands.command(pass_context=True , name = "At",brief = "Sunucudan üye atar.",aliases=["at","kick"])
    async def kick_command(self,ctx,member : discord.Member,reason=None):
          if member != ctx.author :
                if member in ctx.guild.members :
                      if reason==None :
                            reason = "Belirtilmemiş"
                      await member.kick(reason=reason)
                      kick_embed=discord.Embed(title=f"{member.display_name} adlı kullanıcı sunucudan atıldı!",description=f"Sebep : {reason}",colour=0xffd500,timestamp=ctx.message.created_at)
                      file = discord.File("./images/kick.gif", filename="kick.gif")
                      kick_embed.set_image(url="attachment://kick.gif")
                      kick_embed.set_footer(text=f"İstek Sahibi : {ctx.author.display_name}",icon_url=ctx.author.avatar_url)
                      await ctx.send(file=file,embed=kick_embed)
                      logger.info(f"Moderation | Üye Atma : {member} Sunucu : {ctx.guild.name}  | Tarafından : {ctx.author}")
                else :
                      await ctx.send(f"**{member.mention} adlı kullanıcı bu sunucunun bir üyesi değil.**")      
          else :
                await ctx.send(f"**Belirtilen kullanıcı ile istek sahibi aynı olamaz.**")
            
    @commands.guild_only()
    @commands.has_permissions(ban_members=True)
    @commands.bot_has_permissions(ban_members=True)
    @commands.command(pass_context=True ,name="Yasakla" ,brief = "Sunucudan üye yasaklar.",aliases=["yasakla","ban"])
    async def ban_command(self,ctx,member : discord.Member,reason=None):
          if member != ctx.author :
                if ctx.guild.get_member(member.id) is not None :
                     if reason == None :
                           reason = "Belirtilmemiş"
                     await member.ban(reason=reason)
                     ban_embed=discord.Embed(title=f"{member.display_name} adlı kullanıcı sunucudan yasaklandı!",description=f"Sebep : {reason}",colour=0xffd500,timestamp=ctx.message.created_at)
                     file = discord.File("./images/banned.gif", filename="banned.gif")
                     ban_embed.set_image(url="attachment://banned.gif")
                     ban_embed.set_footer(text=f"İstek Sahibi : {ctx.author.display_name}",icon_url=ctx.author.avatar_url)
                     await ctx.send(file=file,embed=ban_embed)
                     logger.info(f"Moderation | Yasaklama : {member} Sunucu : {ctx.guild.name}  | Tarafından : {ctx.author}")
                else :
                     await ctx.send(f"**{member.mention} adlı kullanıcı bu sunucunun bir üyesi değil.**")
          else :
                await ctx.send(f"**Belirtilen kullanıcı ile istek sahibi aynı olamaz.**")

    @commands.guild_only()
    @commands.has_permissions(ban_members=True)
    @commands.bot_has_permissions(ban_members=True)
    @commands.command(pass_context=True , name ="Unban",brief = "Yasaklanan üyenin yasağını kaldırır.",aliases=["unban"])
    async def unban_command(self,ctx,member):
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
                              unban_embed=discord.Embed(title=f"{user} adlı kullanıcının yasaklanması kaldırıldı !",colour=0xffd500,timestamp=ctx.message.created_at)
                              unban_embed.set_footer(text=f"İstek Sahibi : {ctx.author.display_name}",icon_url=ctx.author.avatar_url)
                              await ctx.send(embed=unban_embed)
                              status = True
                              logger.info(f"Moderation | Yasaklama Kaldırma : {member} Sunucu : {ctx.guild.name}  | Tarafından : {ctx.author}")
                  if status == False :
                        unbaner1_embed=discord.Embed(title="Belirtilen kullanıcı yasaklananlar listesinde bulunamadı.",colour=0xffd500)
                        await ctx.send(embed=unbaner1_embed)
         else :
               unbaner2_embed=discord.Embed(title="Üyenin tam adınını giriniz.",description="Örnek : USER#0001",colour=0xffd500)
               await ctx.send(embed=unbaner2_embed)                          

    @commands.guild_only()
    @commands.has_permissions(manage_roles=True)
    @commands.bot_has_permissions(manage_roles=True)
    @commands.command(pass_context=True ,name="Sustur", brief = "Üyeyi susturur.",aliases=["sustur","mute"])
    async def mute_command(self,ctx,member : discord.Member = None):
          role = discord.utils.get(ctx.guild.roles,name = "Susturulmuş")
          if member != ctx.author :
               if member in ctx.guild.members :
                     if role in member.roles :
                           await ctx.send("**Belirtilen üye zaten susturulmuş.**")
                     else :
                           if role == None :
                                 role = await ctx.guild.create_role(name="Susturulmuş")
                                 for channel in ctx.guild.channels:
                                       await channel.set_permissions(role,send_messages = False)
                                 await member.add_roles(role)
                           else :
                                 await member.add_roles(role)
                           mute_embed=discord.Embed(title=f"{member.name} adlı kullanıcı susturuldu !",colour=0xffd500,timestamp=ctx.message.created_at)
                           mute_embed.set_footer(text=f"İstek Sahibi : {ctx.author.display_name}",icon_url=ctx.author.avatar_url)
                           await ctx.send(embed=mute_embed)
                           logger.info(f"Moderation | Susturma : {member} Sunucu : {ctx.guild.name}  | Tarafından : {ctx.author}")      
               else :
                    muteer1_embed=discord.Embed(title=f"{member.name} adlı kullanıcı bu sunucunun bir üyesi değil.",colour=0xffd500)
                    await ctx.send(embed=muteer1_embed)
          else :
                muteer2_embed=discord.Embed(title="Belirtilen kullanıcı ile istek sahibi aynı olamaz.",colour=0xffd500)
                await ctx.send(embed=muteer2_embed)

    @commands.guild_only()
    @commands.has_permissions(manage_roles=True)
    @commands.bot_has_permissions(manage_roles=True)
    @commands.command(pass_context=True ,name = "Unmute" ,brief = "Susturulmuş üyenin yasağını kaldırır.",aliases=["unmute"])   
    async def unmute_command(self,ctx,member : discord.Member = None):
          role = discord.utils.get(ctx.guild.roles,name = "Susturulmuş")
          if member in ctx.guild.members :
               if role != None :
                     if role in member.roles:
                           await member.remove_roles(role)
                           unmute_embed=discord.Embed(title=f"{member.name} adlı kullanıcının susturulma cezası kaldırıldı !",colour=0xffd500,timestamp=ctx.message.created_at)
                           unmute_embed.set_footer(text=f"İstek Sahibi : {ctx.author.display_name}",icon_url=ctx.author.avatar_url)
                           await ctx.send(embed=unmute_embed)
                           logger.info(f"Moderation | Susturma Kaldırma : {member} Sunucu : {ctx.guild.name}  | Tarafından : {ctx.author}")
                     else :
                           unmuteer1_embed=discord.Embed(title=f"{member.name} adlı kullanıcının susturma cezası bulunamadı.",colour=0xffd500)
                           await ctx.send(embed=unmuteer1_embed)
               else :
                     unmuteer2_embed=discord.Embed(title="Daha önceden kimse susturulmamış ya da rol silinmiş olabilir.",colour=0xffd500)
                     await ctx.send(embed=unmuteer2_embed)
          else :
               unmuteer3_embed=discord.Embed(title=f"{member.name} adlı kullanıcı bu sunucunun bir üyesi değil.",colour=0xffd500)
               await ctx.send(embed=unmuteer3_embed)

    @commands.guild_only()
    @commands.has_permissions(change_nickname=True)
    @commands.bot_has_permissions(change_nickname=True)
    @commands.command(pass_context=True ,name="Rename" ,brief = "Üyenin sunucu içindeki takma adını değiştirir.",aliases=["rename"])
    async def rename_command(self,ctx,member : discord.Member,nick):
          if member != ctx.author :
               if member in ctx.guild.members :
                     await member.edit(nick=nick)
                     await ctx.message.add_reaction("\u2705")
               else :
                    renameer1_embed=discord.Embed(title=f"{member.name} adlı kullanıcı bu sunucunun bir üyesi değil.",colour=0xffd500)
                    await ctx.send(embed=renameer1_embed)
          else :
                renameer2_embed=discord.Embed(title="Belirtilen kullanıcı ile istek sahibi aynı olamaz.",colour=0xffd500)
                await ctx.send(embed=renameer2_embed)

def setup(client):
    client.add_cog(Moderation(client))