import crescent
import hikari
import replit

from .database import databases
from .environment import environments
from .model import models

model = models.Model(databases.Database(replit.db))

gateway_bot = hikari.GatewayBot(environments.gateway_bot_token)

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
