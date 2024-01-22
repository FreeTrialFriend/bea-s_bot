import asyncio
import youtube_dl
from discord import *
from discord.ui import Button, View
import discord
from googleapiclient.discovery import build
import os
from subprocess import Popen


# Replace 'YOUR_DISCORD_TOKEN' with your actual Discord bot token
TOKEN = "MTE5NTA2MDk0ODA5NzA1Mjg0Mg.G82Wc9.G3JGVB7C5_hx3eO8FJXcQy3W9OmdEfUWMPcjgo"
# Replace 'YOUR_YOUTUBE_API_KEY' with your actual YouTube Data API key
YOUTUBE_API_KEY = 'AIzaSyD31FxecLwMtKetBGNNBzMjYfgtL4z_y8Y'

# Create a YouTube API client
youtube = build('youtube', 'v3', developerKey=YOUTUBE_API_KEY)


intents = discord.Intents.all()
intents.message_content = True
intents.members = True
client = discord.Client(intents=intents)
bot = Bot(command_prefix="&", intents = intents)

#bdaymsg = "Happy brithday {%s}! Hope you have a good one!!"


@bot.event
async def on_ready():
    await bot.change_presence(activity=discord.Activity(type=discord.ActivityType.watching, name="you :)"))
    print(f'Logged in as {bot.user.name}')

discord.opus.load_opus()

class PlayPauseView(View):
    def __init__(self):
        super().__init__()

    async def on_button_click(self, button, interaction):
        voice_channel = discord.utils.get(interaction.guild.voice_channels, members=[interaction.user])

        if button.label == '▶️ Play':
            if voice_channel and voice_channel.is_paused():
                voice_channel.resume()
        elif button.label == '⏸ Pause':
            if voice_channel and voice_channel.is_playing():
                voice_channel.pause()

        await interaction.defer_update()







@bot.slash_command(name='join', help='Join a voice channel and play a YouTube video')
async def join(ctx, url):
    channel = ctx.author.voice.channel
    voice_channel = await channel.connect()
    
    if 'youtube.com' in url or 'youtu.be' in url:
        # Use youtube_dl to extract information about the video
        with youtube_dl.YoutubeDL() as ydl:
            info = ydl.extract_info(url, download=False)
            url2 = info['formats'][0]['url'] if 'formats' in info else info['url']
        # Play the video in the voice channel
        voice_channel.play(discord.FFmpegPCMAudio(url2, options='-vn'))

    elif 'spotify.com' in url:
        # Use spotdl to download the Spotify track
        os.system(f'spotdl {url}')

        # Get the filename of the downloaded track
        track_file = url.split('/')[-1].split('?')[0] + '.mp3'

        # Play the downloaded track in the voice channel
        voice_channel.play(discord.FFmpegPCMAudio(track_file, options='-vn'))

        # Clean up the downloaded file after playing
        os.remove(track_file)
    else:
        await ctx.respond("Invalid URL. Please provide a valid YouTube or Spotify URL.")
        return
     
    # Send an embed with play and pause buttons
    embed = discord.Embed(title="Music Controls", color=discord.Color.blue())
    view = PlayPauseView()
    view.add_item(Button(label='▶️ Play', custom_id='play_button', style=discord.ButtonStyle.green))
    view.add_item(Button(label='⏸ Pause', custom_id='pause_button', style=discord.ButtonStyle.red))
    await ctx.send(embed=embed, view=view)
    
    
"""@bot.slash_command(name='notify', help='Notify when a specific channel uploads a new video')
async def notify(ctx, channel_id):
    # Implement code to periodically check for new videos from the specified channel
    # Send a message with the link to the new video when found

@bot.slash_command(name='stats', help='Get information/statistics on a YouTube video or channel')
async def stats(ctx, video_id):"""
    # Implement code to retrieve and display information/statistics using the YouTube API

# Run the bot with the token
bot.run(TOKEN)
