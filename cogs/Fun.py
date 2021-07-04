#MIT License
#Copyright (c) 2020 Semih Aydın
#UTF-8

import discord
from discord.ext import commands
import requests
from logging_files.fun_log import logger

class Fun(commands.Cog):
    def __init__(self,client):
        self.client = client

    @commands.cooldown(1, 10, commands.BucketType.user)
    @commands.command(name = "Blurpify",brief = "Kullanıcının profil fotoğrafına Blurpify efekti uygular.",aliases = ["blurpify"])
    async def blurpify_command(self, ctx, member : discord.Member  = None):
        member = member or ctx.author
        url = f"https://nekobot.xyz/api/imagegen?type=blurpify&image={member.avatar_url}"

        req = requests.get(url)
        req_json = req.json()

        if req_json["status"]!= 200:
            blurpifyEmbed = discord.Embed(title="Hata",description ="API bağlantı hatası.",colour = 0xd92929)
            await ctx.send(embed=blurpifyEmbed)

            logger.error(f"Fun | Blurpify | Error: API bağlantısı hatası.")
            return

        blurpifyEmbed_2 = discord.Embed(color=0x36393F)
        blurpifyEmbed_2.set_footer(text=f"Tarafından: {ctx.author}",icon_url=ctx.author.avatar_url)
        blurpifyEmbed_2.set_image(url = req_json["message"])

        await ctx.send(embed=blurpifyEmbed_2)

        logger.info(f"Fun | Blurpify | Tarafından : {ctx.author}")

    @commands.cooldown(1, 10, commands.BucketType.user)
    @commands.command(name = "Captcha",brief = "Kullanıcının profil fotoğrafına Captcha efekti uygular.",aliases = ["captcha"])
    async def captcha_command(self, ctx,text:str,member : discord.Member  = None):
        member = member or ctx.author
        text = text.replace('.',' ')
        url = f"https://nekobot.xyz/api/imagegen?type=captcha&url={member.avatar_url}&username={text}"

        req = requests.get(url)
        req_json = req.json()

        if req_json["status"]!= 200:
            captchaEmbed = discord.Embed(title="Hata",description ="API bağlantı hatası.",colour = 0xd92929)
            await ctx.send(embed=captchaEmbed)

            logger.error(f"Fun | Captcha | Error: API bağlantısı hatası.")
            return

        captchaEmbed_2 = discord.Embed(color=0x36393F)
        captchaEmbed_2.set_footer(text=f"Tarafından: {ctx.author}",icon_url=ctx.author.avatar_url)
        captchaEmbed_2.set_image(url = req_json["message"])

        await ctx.send(embed=captchaEmbed_2)

        logger.info(f"Fun | Captcha | Tarafından : {ctx.author}")

    @commands.cooldown(1, 10, commands.BucketType.user)
    @commands.command(name = "ChangeMyMind",brief = "Girdiğiniz metne ChangeMyMind efekti uygular.",aliases = ["changemymind"])
    async def changemymind_command(self, ctx, *,text:str):
        url = f"https://nekobot.xyz/api/imagegen?type=changemymind&text={text}"

        req = requests.get(url)
        req_json = req.json()

        if req_json["status"]!= 200:
            changeMyMindEmbed = discord.Embed(title="Hata",description ="API bağlantı hatası.",colour = 0xd92929)
            await ctx.send(embed=changeMyMindEmbed)

            logger.error(f"Fun | ChangeMyMind | Error: API bağlantısı hatası.")
            return

        changeMyMindEmbed_2 = discord.Embed(color=0x36393F)
        changeMyMindEmbed_2.set_footer(text=f"Tarafından: {ctx.author}",icon_url=ctx.author.avatar_url)
        changeMyMindEmbed_2.set_image(url = req_json["message"])

        await ctx.send(embed=changeMyMindEmbed_2)

        logger.info(f"Fun | ChangeMyMind | Tarafından : {ctx.author}")

    @commands.cooldown(1, 10, commands.BucketType.user)
    @commands.command(name = "Deepfry",brief = "Kullanıcının profil fotoğrafına Deepfry efekti uygular.",aliases = ["deepfry"])
    async def deepfry_command(self, ctx,member : discord.Member  = None):
        member = member or ctx.author
        url = f"https://nekobot.xyz/api/imagegen?type=deepfry&image={member.avatar_url}"

        req = requests.get(url)
        req_json = req.json()

        if req_json["status"]!= 200:
            deepfryEmbed = discord.Embed(title="Hata",description ="API bağlantı hatası.",colour = 0xd92929)
            await ctx.send(embed=deepfryEmbed)

            logger.error(f"Fun | Deepfry | Error: API bağlantısı hatası.")
            return

        deepfryEmbed_2 = discord.Embed(color=0x36393F)
        deepfryEmbed_2.set_footer(text=f"Tarafından: {ctx.author}",icon_url=ctx.author.avatar_url)
        deepfryEmbed_2.set_image(url = req_json["message"])

        await ctx.send(embed=deepfryEmbed_2)

        logger.info(f"Fun | Deepfry | Tarafından : {ctx.author}")

    @commands.cooldown(1, 10, commands.BucketType.user)
    @commands.command(name = "Kannagen",brief = "Girdiğiniz metne Kannagen efekti uygular.",aliases = ["kannagen"])
    async def kannagen_command(self, ctx, *,text:str):
        url = f"https://nekobot.xyz/api/imagegen?type=kannagen&text={text}"

        req = requests.get(url)
        req_json = req.json()

        if req_json["status"]!= 200:
            kannagenEmbed = discord.Embed(title="Hata",description ="API bağlantı hatası.",colour = 0xd92929)
            await ctx.send(embed=kannagenEmbed)

            logger.error(f"Fun | Kannagen | Error: API bağlantısı hatası.")
            return

        kannagenEmbed_2 = discord.Embed(color=0x36393F)
        kannagenEmbed_2.set_footer(text=f"Tarafından: {ctx.author}",icon_url=ctx.author.avatar_url)
        kannagenEmbed_2.set_image(url = req_json["message"])

        await ctx.send(embed=kannagenEmbed_2)

        logger.info(f"Fun | Kannagen | Tarafından : {ctx.author}")

    @commands.cooldown(1, 10, commands.BucketType.user)
    @commands.command(name = "Phone",brief = "Kullanıcının profil fotoğrafına Phone efekti uygular.",aliases = ["phone"])
    async def phone_command(self, ctx,member : discord.Member  = None):
        member = member or ctx.author
        url = f"https://nekobot.xyz/api/imagegen?type=iphonex&url={member.avatar_url}"

        req = requests.get(url)
        req_json = req.json()

        if req_json["status"]!= 200:
            phoneEmbed = discord.Embed(title="Hata",description ="API bağlantı hatası.",colour = 0xd92929)
            await ctx.send(embed=phoneEmbed)

            logger.error(f"Fun | Phone | Error: API bağlantısı hatası.")
            return

        phoneEmbed_2 = discord.Embed(color=0x36393F)
        phoneEmbed_2.set_footer(text=f"Tarafından: {ctx.author}",icon_url=ctx.author.avatar_url)
        phoneEmbed_2.set_image(url = req_json["message"])

        await ctx.send(embed=phoneEmbed_2)

        logger.info(f"Fun | Phone | Tarafından : {ctx.author}")

    @commands.cooldown(1, 10, commands.BucketType.user)
    @commands.command(name = "Trash",brief = "Kullanıcının profil fotoğrafına Trash efekti uygular.",aliases = ["trash"])
    async def trash_command(self, ctx,member : discord.Member  = None):
        member = member or ctx.author
        url = f"https://nekobot.xyz/api/imagegen?type=trash&url={member.avatar_url}"

        req = requests.get(url)
        req_json = req.json()

        if req_json["status"]!= 200:
            trashEmbed = discord.Embed(title="Hata",description ="API bağlantı hatası.",colour = 0xd92929)
            await ctx.send(embed=trashEmbed)

            logger.error(f"Fun | Trash | Error: API bağlantısı hatası.")
            return

        trashEmbed_2 = discord.Embed(color=0x36393F)
        trashEmbed_2.set_footer(text=f"Tarafından: {ctx.author}",icon_url=ctx.author.avatar_url)
        trashEmbed_2.set_image(url = req_json["message"])

        await ctx.send(embed=trashEmbed_2)

        logger.info(f"Fun | Trash | Tarafından : {ctx.author}")

    @commands.cooldown(1, 10, commands.BucketType.user)
    @commands.command(name = "TrumpTweet",brief = "Girdiğiniz metne TrumpTweet efekti uygular.",aliases = ["trumptweet"])
    async def trumptweet_command(self, ctx, *,text:str):
        url = f"https://nekobot.xyz/api/imagegen?type=trumptweet&text={text}"

        req = requests.get(url)
        req_json = req.json()

        if req_json["status"]!= 200:
            trumpTweetEmbed = discord.Embed(title="Hata",description ="API bağlantı hatası.",colour = 0xd92929)
            await ctx.send(embed=trumpTweetEmbed)

            logger.error(f"Fun | TrumpTweet | Error: API bağlantısı hatası.")
            return

        trumpTweetEmbed_2 = discord.Embed(color=0x36393F)
        trumpTweetEmbed_2.set_footer(text=f"Tarafından: {ctx.author}",icon_url=ctx.author.avatar_url)
        trumpTweetEmbed_2.set_image(url = req_json["message"])

        await ctx.send(embed=trumpTweetEmbed_2)

        logger.info(f"Fun | TrumpTweet | Tarafından : {ctx.author}")

    @commands.cooldown(1, 10, commands.BucketType.user)
    @commands.command(name = "Tweet",brief = "Girdiğiniz metne Tweet efekti uygular.",aliases = ["tweet"])
    async def tweet_command(self, ctx, *,text:str):
        username = ctx.author.name
        url = f"https://nekobot.xyz/api/imagegen?type=tweet&username={username}&text={text}"

        req = requests.get(url)
        req_json = req.json()

        if req_json["status"]!= 200:
            tweetEmbed = discord.Embed(title="Hata",description ="API bağlantı hatası.",colour = 0xd92929)
            await ctx.send(embed=tweetEmbed)

            logger.error(f"Fun | Tweet | Error: API bağlantısı hatası.")
            return

        tweetEmbed_2 = discord.Embed(color=0x36393F)
        tweetEmbed_2.set_footer(text=f"Tarafından: {ctx.author}",icon_url=ctx.author.avatar_url)
        tweetEmbed_2.set_image(url = req_json["message"])

        await ctx.send(embed=tweetEmbed_2)

        logger.info(f"Fun | Tweet | Tarafından : {ctx.author}")

def setup(client):
    client.add_cog(Fun(client))