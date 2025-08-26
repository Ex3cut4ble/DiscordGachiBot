from disnake.ext import commands
from bot.botgui import *
from bot.musicplayer import *

import bot.gachibot

RADIO_GET = "/fisting"

class Gachi(commands.Cog):
    def __init__(self, bot: bot.gachibot.GachiBot):
        self.bot = bot

    @commands.slash_command(name='gachi', description='Включает гачи-радио в голосовом канале')
    async def _gachi_cmd(self, interaction: disnake.ApplicationCommandInteraction):
        voice_client = interaction.guild.voice_client

        if not interaction.user.voice:
            await interaction.response.send_message(embed=build_error_embed("Вы не подключены к голосовому каналу"),
                                                    ephemeral=True)
            return

        if voice_client is not None:
            if voice_client.is_playing():
                await interaction.response.send_message(embed=build_error_embed("Бот уже играет гачи-радио"),
                                                        ephemeral=True)
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
            await interaction.followup.send(
                embed=build_error_embed("Произошла ошибка", "-# Посмотрите консоль бота для подробностей"))

    @commands.slash_command(name='gachi_stop', description='Останавливает гачи-радио.')
    async def _gachi_stop_cmd(self, interaction: disnake.ApplicationCommandInteraction):
        voice_client = interaction.guild.voice_client

        if voice_client is None or not voice_client.is_playing():
            await interaction.response.send_message(embed=build_error_embed("Бот не играет гачи-радио"), ephemeral=True)
            return

        await voice_client.disconnect(force=False)
        await interaction.response.send_message(embed=build_ok_embed("Гачи-радио выключено"))

    @commands.slash_command(name='gachi-search', description='Ищет музыку по введённой фразе.')
    async def _gachi_search_cmd(self, interaction: disnake.ApplicationCommandInteraction, search: str = ""):
        data = self.bot.radio_requester.list_search(search, 1)
        list_embed = build_search_embed(search, 1, data["rows"])
        search_view = SearchSongsView(self.bot.radio_requester, search, 1, data["rows"])
        await interaction.response.send_message(embed=list_embed, view=search_view, ephemeral=True)

    async def _play_gachi(self, interaction: disnake.ApplicationCommandInteraction) -> None:
        await interaction.response.defer(with_message=True)
        music_player = await play_from_url_stream(self.bot.config.get_value("gachi-music-site") + RADIO_GET)
        interaction.guild.voice_client.play(music_player, after=lambda e: print(f'Music player error: {e}') if e else None)
        await interaction.followup.send(embed=build_ok_embed("Гачи-радио включено"))


def setup(bot: bot.gachibot.GachiBot) -> None:
    bot.add_cog(Gachi(bot))
