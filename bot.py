from discord.ext import commands
import discord
import os
from download_music import YTDLSource
import pafy, urllib, re
from discord import FFmpegPCMAudio, PCMVolumeTransformer




class Config:
    TOKEN = 'OTIxMDg0Njc2OTU1ODQ4NzY0.Ybtw8w.dVCcutbdEYrdaIBp975llWwovds'
    PREFIX = '..'


client = commands.Bot(command_prefix=Config.PREFIX)


@client.command()
async def join(ctx):
    # get current channel
    current_channel = discord.utils.get(client.voice_clients, guild=ctx.guild)
    # get the channel which bot should join to
    channel = ctx.message.author.voice.channel
    if current_channel and current_channel.is_connected():
        await current_channel.move_to(channel)

    # connect to channel and save it
    channel = await channel.connect()


@client.event
async def on_ready():
    print('bot.py is ready')

for filename in os.listdir('./cogs'):
    if filename.endswith('.py'):
        client.load_extension(f'cogs.{filename[:-3]}')

client.run(Config.TOKEN)