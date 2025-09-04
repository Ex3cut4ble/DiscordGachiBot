import asyncio

import disnake

from bot.gachibot import GachiBot
from utils.configreader import Config

from aiohttp_socks import ProxyConnector


async def main():
    config = Config("bot_config.cfg")
    token = config.get_value('token')
    if not token or token == 'bot_token_here':
        print('Provide valid bot token.')
        exit(1)

    intents = disnake.Intents.default()
    proxy_url = config.get_value('proxy-url')
    connector = ProxyConnector.from_url(proxy_url) if proxy_url else None
    client = GachiBot(config, intents=intents, connector=connector)
    client.load_extension("cogs.gachi")

    try:
        await client.start(config.get_value('token'))
    except Exception as e:
        print(e)
    finally:
        await client.close()


if __name__ == '__main__':
    asyncio.run(main(), debug=True)
