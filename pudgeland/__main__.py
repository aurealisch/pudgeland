import crescent
import hikari
import collei

from .common import env
from .database import databases
from .module import models

client = collei.Client()
database = databases.Database()

model = models.Model(client, database=database)

gateway_bot = hikari.GatewayBot(env.gateway_bot_token)

gateway_bot.subscribe(hikari.StartedEvent, model.on_started_event)
gateway_bot.subscribe(hikari.StoppedEvent, model.on_stopped_event)

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
