from typing import Any

from discord.app_commands import CommandTree
from discord.ext import tasks

from bot.musicplayer import *
from bot.radiorequests import RadioRequester
from utils.configreader import Config

SITE_KEY = "gachi-music-site"
RADIO_GET = "/fisting"

class GachiBot(discord.Client):
    def __init__(self, config: Config, intents: discord.Intents, **options: Any):
        super().__init__(intents=intents, **options)
        self._config = config
        self._command_tree = CommandTree(self)
        self._radio_requester = RadioRequester(config.get_value(SITE_KEY))

    async def on_ready(self) -> None:
        await self.setup_commands()
        await self._command_tree.sync()

        if not self._status_update.is_running():
            self._status_update.start()

        print(f"Logged on as {self.user}!")

    async def setup_commands(self) -> None:
        @self._command_tree.command(name='gachi', description='Включает гачи-радио в голосовом канале')
        async def _gachi_cmd(interaction: discord.Interaction):
            voice_client = interaction.guild.voice_client

            if not interaction.user.voice:
                await interaction.response.send_message(content="Вы не подключены к голосовому каналу.", ephemeral=True)
                return

            if voice_client is not None:
                if voice_client.is_playing():
                    await interaction.response.send_message(content="Бот уже играет гачи-радио.", ephemeral=True)
                    return
                else:
                    await voice_client.disconnect()
                    voice_client = None

            if voice_client is None:
                await interaction.user.voice.channel.connect()

            try:
                await self._play_gachi(interaction)
            except Exception as ex:
                print(ex)
                await interaction.followup.send(content="Произошла ошибка.\n-# Посмотрите консоль бота для подробностей.")

        @self._command_tree.command(name='gachi_stop', description='Останавливает гачи-радио.')
        async def _gachi_stop(interaction: discord.Interaction):
            voice_client = interaction.guild.voice_client

            if voice_client is None or not voice_client.is_playing():
                await interaction.response.send_message(content="Бот не играет гачи-радио.", ephemeral=True)
                return

            await voice_client.disconnect(force=False)
            await interaction.response.send_message(content="Гачи-радио выключено.")

    @tasks.loop(seconds=20)
    async def _status_update(self) -> None:
        try:
            data = self._radio_requester.request_now_playing()
            title = data["now_playing"]["song"]["title"]
            duration = data["now_playing"]["duration"]
            elapsed = data["now_playing"]["elapsed"]
            timeleft = f"{(elapsed // 60):02}:{(elapsed % 60):02} / {(duration // 60):02}:{(duration % 60):02}"

            played_at = data["now_playing"]["played_at"]
            timestamp = {"start": played_at * 1000, "end": (played_at + duration) * 1000}
            assets = {"large_image": data["now_playing"]["song"]["art"]}

            await self.change_presence(activity=discord.Activity(type=discord.ActivityType.listening, name=title, state=timeleft, assets=assets,
                                                                 timestamps=timestamp, url=self._config.get_value(SITE_KEY)))
        except Exception as ex:
            print(ex)
            await self.change_presence(activity=None)


    async def _play_gachi(self, interaction: discord.Interaction) -> None:
        await interaction.response.defer(thinking=True)
        music_player = await play_from_url_stream(self._config.get_value(SITE_KEY) + RADIO_GET)
        interaction.guild.voice_client.play(music_player, after=lambda e: print(f'Music player error: {e}') if e else None)
        await interaction.followup.send(content="Гачи-радио включено.")
