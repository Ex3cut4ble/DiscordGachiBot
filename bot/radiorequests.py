from urllib import parse

import requests

NOW_PLAYING_GET = "/api/nowplaying/gachibass_radio"
LIST_SEARCH_GET = "/api/station/1/requests?internal=true&flushCache=true"
REQUEST_SONG_GET = "/api/station/1/request/"

class RadioRequester:
    def __init__(self, url: str):
        self._url = url

    def request_now_playing(self) -> dict:
        response = requests.get(url=(self._url + NOW_PLAYING_GET))
        if response.status_code != 200:
            print(response.status_code, response.reason)
            raise Exception(f"{self._url + NOW_PLAYING_GET} GET request failed ({response.status_code}): {response.reason}")

        return response.json()

    def list_search(self, search: str = "", page: int = 1, row_count: int = 10) -> dict:
        get_url = self._build_search_get(search, page, row_count)
        response = requests.get(url=get_url)
        if response.status_code != 200:
            print(response.status_code, response.reason)
            raise Exception(f"{get_url} GET request failed ({response.status_code}): {response.reason}")

        return response.json()

    def request_song(self, song_name: str) -> int:
        data = self.list_search(song_name)
        if len(data["rows"] < 1):
            raise Exception(f"Song \"{song_name}\" not found on site {self._url}")

        return self.request_song_by_id(data["rows"][0]["request_id"])

    def request_song_by_id(self, song_id: str) -> int:
        response = requests.get(url=(self._url + REQUEST_SONG_GET + song_id))
        return response.status_code

    def _build_search_get(self, search: str, page: int, row_count: int):
        search_encoded = parse.quote_plus(search, safe="()[]")
        return self._url + LIST_SEARCH_GET + f"&rowCount={row_count}&current={page}&searchPhrase={search_encoded}"
