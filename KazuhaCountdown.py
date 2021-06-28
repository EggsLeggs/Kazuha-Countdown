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

channelEU = None
channelAsia = None
channelNA = None
timeEU = datetime.strptime('2021-06-29-17',"%Y-%m-%d-%H")
timeAsia = datetime.strptime('2021-06-29-10',"%Y-%m-%d-%H")
timeNA = datetime.strptime('2021-06-29-23',"%Y-%m-%d-%H")

@bot.event
async def on_ready():
    print('Ready')

@bot.command()
@commands.is_owner()
async def activateEU(ctx, channelID):
    print("activate started")
    global channelEU
    channelEU = await bot.fetch_channel(int(channelID))
    update_channelEU.start()
    bot.timer_manager.create_timer('countdownEndEU', timeEU)
    print("activate executed")

@bot.command()
@commands.is_owner()
async def activateAsia(ctx, channelID):
    print("activate started")
    global channelAsia
    channelAsia = await bot.fetch_channel(int(channelID))
    update_channelAsia.start()
    bot.timer_manager.create_timer('countdownEndAsia', timeAsia)
    print("activate executed")

@bot.command()
@commands.is_owner()
async def activateNA(ctx, channelID):
    print("activate started")
    global channelNA
    channelNA = await bot.fetch_channel(int(channelID))
    update_channelNA.start()
    bot.timer_manager.create_timer('countdownEndNA', timeNA)
    print("activate executed")

@tasks.loop(hours=1)
async def update_channelEU():
    print("update channel started")
    rd = relativedelta(timeEU, datetime.utcnow()).__dict__
    if (rd['days'] != 1) and (rd['hours'] != 1):
        await channelEU.edit(name = "EU: %(days)d Days %(hours)d Hours" % rd)
    elif (rd['days'] == 1) and (rd['hours'] != 1):
        await channelEU.edit(name = "EU: %(days)d Day %(hours)d Hours" % rd)
    elif (rd['days'] != 1) and (rd['hours'] == 1):
        await channelEU.edit(name = "EU: %(days)d Days %(hours)d Hour" % rd)
    else:
        await channelEU.edit(name = "EU: %(days)d Day %(hours)d Hour" % rd)
    print("update channel executed")

@tasks.loop(hours=1)
async def update_channelAsia():
    print("update channel started")
    rd = relativedelta(timeAsia, datetime.utcnow()).__dict__
    if (rd['days'] != 1) and (rd['hours'] != 1):
        await channelAsia.edit(name = "Asia: %(days)d Days %(hours)d Hours" % rd)
    elif (rd['days'] == 1) and (rd['hours'] != 1):
        await channelAsia.edit(name = "Asia: %(days)d Day %(hours)d Hours" % rd)
    elif (rd['days'] != 1) and (rd['hours'] == 1):
        await channelAsia.edit(name = "Asia: %(days)d Days %(hours)d Hour" % rd)
    else:
        await channelAsia.edit(name = "Asia: %(days)d Day %(hours)d Hour" % rd)
    print("update channel executed")

@tasks.loop(hours=1)
async def update_channelNA():
    print("update channel started")
    rd = relativedelta(timeNA, datetime.utcnow()).__dict__
    if (rd['days'] != 1) and (rd['hours'] != 1):
        await channelNA.edit(name = "NA: %(days)d Days %(hours)d Hours" % rd)
    elif (rd['days'] == 1) and (rd['hours'] != 1):
        await channelNA.edit(name = "NA: %(days)d Day %(hours)d Hours" % rd)
    elif (rd['days'] != 1) and (rd['hours'] == 1):
        await channelNA.edit(name = "NA: %(days)d Days %(hours)d Hour" % rd)
    else:
        await channelNA.edit(name = "NA: %(days)d Day %(hours)d Hour" % rd)
    print("update channel executed")
    
@bot.event
async def on_countdownEndEU():
    print("delete channel started")
    update_channel.cancel()
    await channelEU.delete()
    update_channelEU.stop()
    print("delete channel executed")

@bot.event
async def on_countdownEndAsia():
    print("delete channel started")
    update_channel.cancel()
    await channelAsia.delete()
    update_channelAsia.stop()
    print("delete channel executed")

@bot.event
async def on_countdownEndNA():
    print("delete channel started")
    update_channel.cancel()
    await channelNA.delete()
    update_channelNA.stop()
    print("delete channel executed")

#------------------------------------------------------------------------------#
bot.run(kazuConfig.discordKey)
