import discord
from discord.ext import commands
import youtube_dl
import os
from dotenv import load_dotenv

intents = discord.Intents.default()

#TODO: check installed site-packages - are all of them needed?

# Take environment variables from .env file
load_dotenv()

# Discord Token
DISCORD_TOKEN = os.getenv("DISCORD_TOKEN")

# make a Client and a Bot instances
client = discord.Client(intents=intents)
bot = commands.Bot(command_prefix='~', intents=intents)

@client.event
async def on_message(message):
    message.content = message.content.lower()
    if message.author == client.user:
        return
    if message.content.startswith(("привет", "ку", "hello", "hi", "hey")):
        await message.channel.send(f"*Гавкает по-тюленьи* (Привет, {message.author}!)")
        with open(r'.\assets\hello\hey1.gif', 'rb') as file:
            hello_picture = discord.File(file)
            await message.channel.send(file=hello_picture)

# TODO: check if this function works
@bot.event
async def on_member_join(member):
        with open(r'.\assets\hello\hey-gif.gif', 'rb') as file:
            hello_picture = discord.File(file)
            await message.channel.send(file=hello_picture)

@bot.command()
async def play(context, url:str, channel="Основной"):
    music_check = os.path.isfile("music.mp3")
    try:
        if music_check: os.remove("music.mp3")
    except PermissionError:
        await context.send(f"Дождитесь завершения играющей музыки или используйте"
                           " команду {bot.command_prefix}stop")
        # return

    voice_channel = discord.utils.get(context.guild.voice_channels,
                                      name=channel)
    try: await voice_channel.connect()
    except: await context.send("Бот уже присоединенлся к каналу")
    voice_client = discord.utils.get(client.voice_clients, guild=context.guild)
    # else: voice_client.move_to(channel)

    ydl_options = {
        "format": "bestaudio/best",
        "postprocessor": [{
            "key": "FFmpegExtractAudio",
            "preferredcodec": "mp3",
            "preferredquality": "192",
        }]
    }
    with youtube_dl.YoutubeDL(ydl_options) as ytdl:
        ytdl.download([url])

    for file in os.listdir(".\\"):
        if file.endswith((".m4a", ".webm")):
            os.rename(file, "music.mp3")

    context.message.guild.voice_client.play(
        discord.FFmpegPCMAudio(executable="ffmpeg.exe",
                               source=".\music.mp3"))
    # voice_client.play(discord.FFmpegPCMAudio(executable="ffmpeg.exe",
    #                                          source="music.mp3"))

@bot.command()
async def leave(context):
    voice_client = discord.utils.get(client.voice_clients, guild=context.guild)
    if voice_client.connected(): await voice_channel.dicconnect()
    else: context.send("Я не подключен к этому каналу")

@bot.command()
async def pause(context):
    voice_client = discord.utils.get(client.voice_clients, guild=context.guild)
    if voice_client.is_playing(): voice_client.pause()
    else: context.send("Сейчас ничего не играет")

@bot.command()
async def resume(context):
    voice_client = discord.utils.get(client.voice_clients, guild=context.guild)
    if voice_client.is_paused(): voice.resume()
    else: context.send("Музыка не стоит на паузе")

@bot.command()
async def stop(context):
    voice_client = discord.utils.get(client.voice_clients, guild=context.guild)
    if voice_client.is_playing(): voice_client.stop()
    else: context.send("Сейчас ничего не играет")

# 🎶

if __name__ == '__main__':
    # run a Client
    bot.run(DISCORD_TOKEN)
    client.run(DISCORD_TOKEN)
