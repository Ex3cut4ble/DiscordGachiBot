import discord

from bot.gachibot import GachiBot
from utils.configreader import Config


def main():
    config = Config("bot_config.cfg")
    intents = discord.Intents.default()
    client = GachiBot(config, intents=intents)
    client.run(config.get_value('token'))

if __name__ == '__main__':
    main()