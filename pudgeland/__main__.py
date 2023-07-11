import crescent
import hikari

from .env import envs

gateway_bot = hikari.GatewayBot(envs.gateway_bot_token)

client = crescent.Client(gateway_bot)

plugins = {
    "pudgeland.plugin.action.bite",
    "pudgeland.plugin.action.hug",
    "pudgeland.plugin.action.kiss",
    "pudgeland.plugin.action.lick",
    "pudgeland.plugin.server.query",
}

for plugin in plugins:
    client.plugins.load(plugin)

gateway_bot.run()
