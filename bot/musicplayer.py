import disnake

FFMPEG_OPTIONS = {
    'before_options': '-reconnect 1 -reconnect_streamed 1 -reconnect_delay_max 5',
    'options': '-vn'
}

async def play_from_url_stream(url):
    return disnake.FFmpegPCMAudio(url, **FFMPEG_OPTIONS)
