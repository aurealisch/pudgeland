import crescent
import hikari
import collei

from .env import envs
from .model import models

client = collei.Client()

model = models.Model(client)

gateway_bot = hikari.GatewayBot(envs.gateway_bot_token)

client = crescent.Client(gateway_bot, model=model)

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
