from discord.ext import commands
import discord
import pafy, urllib, re
from discord import FFmpegPCMAudio, PCMVolumeTransformer

FFMPEG_OPTIONS = {'before_options': '-reconnect 1 -reconnect_streamed 1 -reconnect_delay_max 5','options': '-vn'}

class Music(commands.Cog):
    def __init__(self,client):
        self.client = client
        self.queue = []
    
    @commands.Cog.listener()
    async def on_ready(self):
        print('Music Cog is ready')
    
    @commands.command()
    async def play(self, ctx, music_name):

        voice_client = await self.join_channel(ctx)

        video_ids = self.search_music(music_name)
        
        await ctx.send("https://www.youtube.com/watch?v=" + video_ids[0])
        # creates a new pafy object
        song = pafy.new(video_ids[0])
        # gets an audio source
        audio = song.getbestaudio()  
        # converts the youtube audio source into a source discord can use
        source = FFmpegPCMAudio(audio.url, **FFMPEG_OPTIONS)  
        # initialize the source class variable
        voice_client.play(source)  
    
    @commands.command()
    async def pause(self, ctx):
        # get voice client
        voice_client, voice = await self.create_voice_client(ctx)
        # pause the music
        voice_client.pause()
    
    @commands.command()
    async def resume(self, ctx):
        # get voice client
        voice_client, voice = await self.create_voice_client(ctx)
        # resume the music
        voice_client.resume()

    @commands.command()
    async def stop(self, ctx):
        # get voice client
        voice_client, voice = await self.create_voice_client(ctx)
        # stop the music
        voice_client.stop()


    def search_music(self,music_name):
    
        # save music name in a search variable
        search = music_name
        search = search.replace(" ", "+")
        # create proper url and open it and save the response as html
        html = urllib.request.urlopen("https://www.youtube.com/results?search_query=" + search)
        video_ids = re.findall(r"watch\?v=(\S{11})", html.read().decode())

        return video_ids

    async def join_channel(self,ctx):
        voice_client, voice = await self.create_voice_client(ctx)
         # find the channel that user in it
        channel = ctx.message.author.voice.channel
        # if current channel is exist then we move the bot to new channel otherwise bot join to new voice channel
        if voice_client == None:
            voice_client = await voice.connect()
        else:
            await voice_client.move_to(channel)
        return voice_client

    async def create_voice_client(self, ctx):
         # when the user is not in voice channel
        if ctx.message.author.voice == None:
            await ctx.send(embed=discord.Embeds.txt("No Voice Channel", "You need to be in a voice channel to use this command!", ctx.author))
            return
        # find the channel that user in it
        channel = ctx.message.author.voice.channel

        voice = discord.utils.get(ctx.guild.voice_channels, name=channel.name)
        # get current channel
        voice_client = discord.utils.get(self.client.voice_clients, guild=ctx.guild)

        return voice_client, voice



        

def setup(client):
    client.add_cog(Music(client=client))
