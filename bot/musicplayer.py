import discord

FFMPEG_OPTIONS = {
    'options': '-vn'
}

class MusicPlayer(discord.PCMVolumeTransformer):
    def __init__(self, source, *, data, volume=0.5):
        super().__init__(source, volume)
        self.data = data

    @classmethod
    async def play_from_url_stream(cls, url):
        data = dict()
        data['url'] = url
        return cls(discord.FFmpegPCMAudio(url, **FFMPEG_OPTIONS), data=data)


async def play_from_url_stream_test(url):
    return discord.FFmpegPCMAudio(url, **FFMPEG_OPTIONS)