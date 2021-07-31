import os
import discord
from discord.ext import commands
import requests
import youtube_dl
from dotenv import load_dotenv



# TODO: check installed site-packages - are all of them needed?
# TODO: implement playlist (add track, view list, delete track)
# FOR NOW GENERATES EXCEPTION:
# discord.ext.commands.errors.CommandInvokeError: Command raised an exception: ClientException: Already playing audio.
# TODO: on_member_join function not working?
# TODO: implement "help" message with main commands



# Dictate intents for the bot
intents = discord.Intents.default()
intents.members = True

# Take environment variables from .env file
load_dotenv()

# Discord Token
DISCORD_TOKEN = os.getenv("DISCORD_TOKEN")

# make a Client and a Bot instances
client = discord.Client(intents=intents)
bot = commands.Bot(command_prefix='~', intents=intents)

@bot.event
async def on_ready():
    print("BOT online")

@bot.event
async def on_message(message):
    await bot.process_commands(message)
    message.content = message.content.lower()
    if message.author == bot.user:
        return
    if message.content.startswith(("привет", "ку", "hello", "hi", "hey")):
        await message.channel.send(f"Привет, {message.author}!")
        with open(r'.\assets\hello\hey1.gif', 'rb') as file:
            hello_picture = discord.File(file)
            await message.channel.send(file=hello_picture)

# On new member joining server
@bot.event
async def on_member_join(member):
    channel = client.get_channel("Основной")
    await channel.send(f"Добро пожаловать на сервер, {member}!")

@bot.command()
async def join(ctx):
    channel = ctx.author.voice.channel
    voice = discord.utils.get(bot.voice_clients, guild=ctx.guild)
    if voice and voice.is_connected():
        await voice.move_to(channel)
    else:
        await channel.connect()

def search(query):
    with youtube_dl.YoutubeDL({'format': 'bestaudio'}) as ydl: # , 'noplaylist':'True'
        try:    requests.get(query)
        except: info = ydl.extract_info(f"ytsearch:{query}", download=False)['entries'][0]
        else:   info = ydl.extract_info(query, download=False)
    return (info, info['formats'][0]['url'])

@bot.command()
async def play(ctx, *, query):
    # Reconnect to avoid problems with streaming data from youtube
    FFMPEG_OPTS = {'before_options': '-reconnect 1 -reconnect_streamed 1 -reconnect_delay_max 5', 'options': '-vn'}

    video, source = search(query)
    voice = discord.utils.get(bot.voice_clients, guild=ctx.guild)

    # await join(ctx)

    voice.play(discord.FFmpegPCMAudio(source, **FFMPEG_OPTS), after=lambda e: print('done', e))
    voice.is_playing()
    await ctx.send(f"Now playing 🎶 {video['title']}.")

@bot.command()
async def leave(ctx):
    voice_client = discord.utils.get(ctx.bot.voice_clients, guild=ctx.guild)
    print(voice_client)
    # None being the default value if the bot isn't in a channel
    # (which is why the is_connected() is returning errors)
    if voice_client != None:
        print("disconnected")
        await ctx.voice_client.disconnect()
    else:
        await ctx.send("Я не подключен к этому каналу")

@bot.command()
async def pause(ctx):
    voice_client = discord.utils.get(bot.voice_clients, guild=ctx.guild)
    if voice_client.is_playing(): voice_client.pause()
    else: ctx.send("Сейчас ничего не играет")

@bot.command()
async def resume(ctx):
    voice_client = discord.utils.get(bot.voice_clients, guild=ctx.guild)
    if voice_client.is_paused(): voice_client.resume()
    else: ctx.send("Сейчас ничего не играет")

@bot.command()
async def stop(ctx):
    voice_client = discord.utils.get(bot.voice_clients, guild=ctx.guild)
    if voice_client.is_playing(): voice_client.stop()
    else: ctx.send("Сейчас ничего не играет")




if __name__ == '__main__':
    # run the bot
    #client.run(DISCORD_TOKEN)
    bot.run(DISCORD_TOKEN)
