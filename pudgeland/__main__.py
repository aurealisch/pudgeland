import crescent
import hikari

from .common import env
from .database import databases
from .modules import models

model = models.Model(databases.Database())

gateway_bot = hikari.GatewayBot(env.gateway_bot_token)

gateway_bot.subscribe(hikari.StartedEvent, model.on_started_event)
gateway_bot.subscribe(hikari.StoppedEvent, model.on_stopped_event)

client = crescent.Client(gateway_bot, model=model)

plugins = {
    "pudgeland.plugins.server.query",
}

for plugin in plugins:
    client.plugins.load(plugin)

gateway_bot.run()
