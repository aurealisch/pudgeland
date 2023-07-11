import crescent
import hikari

from .common import env

gateway_bot = hikari.GatewayBot(env.gateway_bot_token)

client = crescent.Client(gateway_bot)

plugins = {
    "pudgeland.plugins.server.query",
    "pudgeland.plugins.voice.create",
    "pudgeland.plugins.voice.delete",
}

for plugin in plugins:
    client.plugins.load(plugin)

gateway_bot.run()
