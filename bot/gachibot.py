from typing import Any

from disnake.ext import tasks, commands

from bot.musicplayer import *
from bot.radiorequests import RadioRequester
from utils.configreader import Config


class GachiBot(commands.InteractionBot):
    def __init__(self, config: Config, **options: Any):
        super().__init__(**options)
        self.config = config
        self.radio_requester = RadioRequester(config.get_value("gachi-music-site"))

    async def on_ready(self) -> None:
        if not self._status_update.is_running():
            self._status_update.start()

        print(f"Logged on as {self.user}!")

    @tasks.loop(seconds=20)
    async def _status_update(self) -> None:
        try:
            data = self.radio_requester.request_now_playing()
            title = data["now_playing"]["song"]["title"]
            duration = data["now_playing"]["duration"]
            elapsed = data["now_playing"]["elapsed"]
            timeleft = f"{(elapsed // 60):02}:{(elapsed % 60):02} / {(duration // 60):02}:{(duration % 60):02}"

            played_at = data["now_playing"]["played_at"]
            timestamp = {"start": played_at * 1000, "end": (played_at + duration) * 1000}
            assets = {"large_image": data["now_playing"]["song"]["art"]}

            await self.change_presence(activity=disnake.Activity(type=disnake.ActivityType.listening, name=title, state=timeleft, assets=assets,
                                                                 timestamps=timestamp, url=self.config.get_value("gachi-music-site")))
        except Exception as ex:
            print(ex)
            await self.change_presence(activity=None)



