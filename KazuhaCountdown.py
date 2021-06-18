import discord
from discord.ext import commands, tasks, timers
from discord.ext.commands import is_owner
from datetime import datetime
from dateutil.relativedelta import relativedelta
import sys
import kazuConfig
#----------------------------------------------------------------
description = "This bot is strictly for setting up a countdown channel in Kazuha Mains"
intents = discord.Intents.default()
activity = discord.Activity(type=discord.ActivityType.watching, name="discord.gg/kazuhamains")
bot = commands.Bot(command_prefix="KC$", activity=activity, description=description, intents=intents)
bot.timer_manager = timers.TimerManager(bot)

channel = None
time = datetime.strptime('2021-06-29-18',"%Y-%m-%d-%H")

@bot.event
async def on_ready():
    print('Ready')

@bot.command()
@commands.is_owner()
async def activate(ctx, channelID):
    print("activate started")
    global channel
    channel = await bot.fetch_channel(int(channelID))
    update_channel.start()
    bot.timer_manager.create_timer('countdownEnd', time)
    print("activate executed")

@tasks.loop(hours=1)
async def update_channel():
    print("update channel started")
    rd = relativedelta(time, datetime.utcnow()).__dict__
    if (rd['days'] != 1) and (rd['hours'] != 1):
        await channel.edit(name = "%(days)d Days %(hours)d Hours" % rd)
    elif (rd['days'] == 1) and (rd['hours'] != 1):
        await channel.edit(name = "%(days)d Day %(hours)d Hours" % rd)
    elif (rd['days'] != 1) and (rd['hours'] == 1):
        await channel.edit(name = "%(days)d Days %(hours)d Hour" % rd)
    else:
        await channel.edit(name = "%(days)d Day %(hours)d Hour" % rd)
    print("update channel executed")
    
@bot.event
async def on_countdownEnd():
    print("delete channel started")
    update_channel.cancel()
    await channel.delete()
    sys.exit()
    print("delete channel executed")

#------------------------------------------------------------------------------#
bot.run(kazuConfig.discordKey)
