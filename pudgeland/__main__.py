import crescent
import hikari

from .common import config

gateway_bot = hikari.GatewayBot(config.discord_gateway_bot_token)

client = crescent.Client(gateway_bot)

plugins = {"pudgeland.plugins.server.status"}

for plugin in plugins:
    client.plugins.load(plugin)

gateway_bot.run()
