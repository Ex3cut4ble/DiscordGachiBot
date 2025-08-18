import disnake
from disnake import Embed

from bot.radiorequests import RadioRequester


def build_search_embed(search: str, page: int, songs: dict) -> Embed:
    if len(songs) < 1:
        empty_embed = Embed(color=0xFF0000, title="Музыка по запросу не найдена")
        return empty_embed

    embed = Embed(color=0x0000FF, title=f"Список музыки (страница #{page})")
    embed.set_footer(text=f"Запрос: \"{search}\"")
    description = ""
    limit = len(songs) if len(songs) < 10 else 10
    for i in range(0, limit):
        description += f"`{i + 1})` **{songs[i]['song']['title']}**\n"
    embed.description = description

    return embed

def build_song_embed(color: int, title: str, description: str, artist: str, art: str, requester_name: str = "", duration: int | None = None) -> Embed:
    embed = Embed(title=title, color=color)
    desc = f"*by* ***{artist}***\n{description}"
    if duration is not None:
        desc += f"\n`[{duration // 60}:{duration % 60}]`"

    embed.description = desc
    embed.set_image(url=art)
    embed.set_footer(text=requester_name)

    return embed

def build_error_embed(title: str, description: str = "") -> Embed:
    return Embed(color=0xFF0000, title=title, description=description)

def build_ok_embed(title: str, description: str = "") -> Embed:
    return Embed(color=0x00FF00, title=title, description=description)


class SearchSongsView(disnake.ui.View):
    def __init__(self, requester: RadioRequester, search_song: str, page: int, songs: dict):
        super().__init__()
        self._search = search_song
        self._radio_requester = requester
        self._page = page
        self._songs = songs
        self.add_item(SongSelection(requester, songs))

    @disnake.ui.button(label='Предыдущая страница ⏪', row=1)
    async def prev_page(self, interaction: disnake.Interaction, button: disnake.ui.Button):
        if self._page - 1 < 1:
            return

        data = self._radio_requester.list_search(self._search, self._page - 1)
        search_view = SearchSongsView(self._radio_requester, self._search, self._page - 1, data["rows"])
        await interaction.response.edit_message(embed=build_search_embed(self._search, self._page - 1, data["rows"]), view=search_view)

    @disnake.ui.button(label='Следующая страница ⏩', row=1)
    async def next_page(self, interaction: disnake.Interaction, button: disnake.ui.Button):
        data = self._radio_requester.list_search(self._search, self._page + 1)
        if len(data["rows"]) < 1:
            return

        search_view = SearchSongsView(self._radio_requester, self._search, self._page + 1, data["rows"])
        await interaction.response.edit_message(embed=build_search_embed(self._search, self._page + 1, data["rows"]), view=search_view)


class SongSelection(disnake.ui.Select):
    def __init__(self, radio_requester: RadioRequester, songs: dict):
        super().__init__(row=2)
        self._radio_requester = radio_requester
        self._choose_songs = dict()
        limit = len(songs) if len(songs) < 10 else 10
        for i in range(0, limit):
            self._choose_songs[songs[i]["request_id"]] = {
                "title": songs[i]["song"]["title"],
                "art": songs[i]["song"]["art"],
                "artist": songs[i]["song"]["artist"]
            }
            self.add_option(label=f"{i + 1}", value=f"{songs[i]['request_id']}", description=f"Заказать {i + 1}-й трек из списка")

    async def callback(self, interaction: disnake.Interaction):
        song_id = self.values[0]
        status = self._radio_requester.request_song_by_id(song_id)
        if status == 200:
            song_embed = build_song_embed(0xF020D8, "Трек заказан",
                                          self._choose_songs[song_id]["title"], self._choose_songs[song_id]["artist"], self._choose_songs[song_id]["art"], interaction.user.name)
            await interaction.response.send_message(embed=song_embed)
        elif status == 500:
            await interaction.response.send_message(embed=build_error_embed("Не удалось заказать трек",
             "Вероятно, недавно (< 2-х минут назад) бот уже заказывал трек, или выбранный трек кем-то недавно уже был заказан на радио, или выбранный трек уже находится в очереди."),
                ephemeral=True)
        else:
            print(f"Error in requesting track, status code: {status}")
            await interaction.response.send_message(embed=build_error_embed("Не удалось заказать трек", "Неизвестная ошибка."), ephemeral=True)
