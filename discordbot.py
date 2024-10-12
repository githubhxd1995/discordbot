import os
import discord
from discord.ext import commands

from qinglong import update_jd_cookie
from qinglong import update_jd_cookie_only_by_cookie
from qinglong import add_jd_cookie


token = os.environ['DISCORD_BOT_TOKEN']
intents = discord.Intents.default()
intents.message_content = True

bot=commands.Bot(command_prefix='!',intents=intents)

@bot.command()
@commands.has_permissions(administrator=True)
async def synccommands(ctx):
    await bot.tree.sync()
    await ctx.send('同步成功')






@bot.hybrid_command()
async def update_cookie(ctx,cookie:str):
    """更新cookies,不需要指定用户"""
    result = update_jd_cookie_only_by_cookie(cookie)
    await ctx.send(result)

@bot.hybrid_command()
async def add_cookie(ctx,cookie:str):
    """新增一个cookie"""
    result = add_jd_cookie(cookie)
    await ctx.send(result)

bot.run(token)