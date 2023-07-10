import crescent
import hikari

from .common import environ

gateway_bot = hikari.GatewayBot(environ.GATEWAY_BOT_TOKEN)

client = crescent.Client(gateway_bot)

plugins = {
    "pudgeland.plugins.server.status",
    "pudgeland.plugins.voice.create",
    "pudgeland.plugins.voice.delete",
}

for plugin in plugins:
    client.plugins.load(plugin)

gateway_bot.run()
