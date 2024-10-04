import requests

NOW_PLAYING_GET = "/api/nowplaying/gachibass_radio"

class RadioRequester:
    def __init__(self, url: str):
        self._url = url

    def request_now_playing(self) -> dict:
        response = requests.get(url=(self._url + NOW_PLAYING_GET))
        if response.status_code != 200:
            print(response.status_code, response.reason)
            raise Exception(f"{self._url + NOW_PLAYING_GET} GET request failed ({response.status_code}): {response.reason}")

        return response.json()