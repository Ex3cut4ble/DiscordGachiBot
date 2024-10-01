import discord

FFMPEG_OPTIONS = {
    'options': '-vn'
}

async def play_from_url_stream(url):
    return discord.FFmpegPCMAudio(url, **FFMPEG_OPTIONS)