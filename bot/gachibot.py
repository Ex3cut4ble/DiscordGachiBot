from typing import Any

from disnake.ext import tasks, commands

from bot.botgui import *
from bot.musicplayer import *
from bot.radiorequests import RadioRequester
from utils.configreader import Config

SITE_KEY = "gachi-music-site"
RADIO_GET = "/fisting"

class GachiBot(commands.InteractionBot):
    def __init__(self, config: Config, **options: Any):
        super().__init__(**options)
        self._config = config
        self._radio_requester = RadioRequester(config.get_value(SITE_KEY))

    async def on_ready(self) -> None:
        await self.setup_commands()
        await self._sync_application_commands()

        if not self._status_update.is_running():
            self._status_update.start()

        print(f"Logged on as {self.user}!")

    async def setup_commands(self) -> None:
        @self.slash_command(name="test")
        async def test(interaction: disnake.ApplicationCommandInteraction):
            await interaction.response.defer(with_message=True)
            await interaction.send(content="pong")

        @self.slash_command(name='gachi', description='Включает гачи-радио в голосовом канале')
        async def _gachi_cmd(interaction: disnake.ApplicationCommandInteraction):
            voice_client = interaction.guild.voice_client

            if not interaction.user.voice:
                await interaction.response.send_message(embed=build_error_embed("Вы не подключены к голосовому каналу"), ephemeral=True)
                return

            if voice_client is not None:
                if voice_client.is_playing():
                    await interaction.response.send_message(embed=build_error_embed("Бот уже играет гачи-радио"), ephemeral=True)
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
                await interaction.followup.send(embed=build_error_embed("Произошла ошибка", "-# Посмотрите консоль бота для подробностей"))

        @self.slash_command(name='gachi_stop', description='Останавливает гачи-радио.')
        async def _gachi_stop_cmd(interaction: disnake.ApplicationCommandInteraction):
            voice_client = interaction.guild.voice_client

            if voice_client is None or not voice_client.is_playing():
                await interaction.response.send_message(embed=build_error_embed("Бот не играет гачи-радио"), ephemeral=True)
                return

            await voice_client.disconnect(force=False)
            await interaction.response.send_message(embed=build_ok_embed("Гачи-радио выключено"))

        @self.slash_command(name='gachi-search', description='Ищет музыку по введённой фразе.')
        async def _gachi_search_cmd(interaction: disnake.ApplicationCommandInteraction, search: str = ""):
            data = self._radio_requester.list_search(search, 1)
            list_embed = build_search_embed(search, 1, data["rows"])
            search_view = SearchSongsView(self._radio_requester, search, 1, data["rows"])
            await interaction.response.send_message(embed=list_embed, view=search_view, ephemeral=True)


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

            await self.change_presence(activity=disnake.Activity(type=disnake.ActivityType.listening, name=title, state=timeleft, assets=assets,
                                                                 timestamps=timestamp, url=self._config.get_value(SITE_KEY)))
        except Exception as ex:
            print(ex)
            await self.change_presence(activity=None)


    async def _play_gachi(self, interaction: disnake.ApplicationCommandInteraction) -> None:
        await interaction.response.defer(with_message=True)
        music_player = await play_from_url_stream(self._config.get_value(SITE_KEY) + RADIO_GET)
        interaction.guild.voice_client.play(music_player, after=lambda e: print(f'Music player error: {e}') if e else None)
        await interaction.followup.send(embed=build_ok_embed("Гачи-радио включено"))
