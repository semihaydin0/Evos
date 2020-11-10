import discord
from discord.ext import commands

from logging_files.math_log import logger

class Math(commands.Cog):
    def __init__(self,client):
        self.client = client

    @commands.command(pass_context=True,name="Hesapla",brief= "İki sayı ile dört işlem yapar.",aliases = ['hesapla','işlem'])
    async def math_command(self,ctx,num1 : int ,op,num2: int):
        result = 0.0
        if op == "+":
            result = num1 + num2
            await ctx.send(f"{num1}{op}{num2} işleminin sonucu = **{result}**")
        elif op == "-":
            result = num1 - num2
            await ctx.send(f"{num1}{op}{num2} işleminin sonucu = **{result}**")
        elif op == "*":
            result = num1 * num2
            await ctx.send(f"{num1}{op}{num2} işleminin sonucu = **{result}**")
        elif op == "/":
            result = num1 / num2
            await ctx.send(f"{num1}{op}{num2} işleminin sonucu = **{result}**")
        else : 
            await ctx.send(f"**Hatalı operatör girişi.(Sadece + - * /)**")
        logger.info(f"Math | Hesapla | Tarafından : {ctx.author}")

def setup(client):
    client.add_cog(Math(client))