import crescent
import hikari
import prisma

from .database import databases
from .environment import environments
from .model import models

gateway_bot = hikari.GatewayBot(environments.gateway_bot_token)

model = models.Model(databases.Database(prisma.Prisma()))
prisma.register(model.database.prisma)

gateway_bot.subscribe(hikari.StartedEvent, model.on_started_event)
gateway_bot.subscribe(hikari.StoppedEvent, model.on_stopped_event)

client = crescent.Client(gateway_bot, model=model)

client.plugins.load_folder("pudgeland.plugin.action")
client.plugins.load_folder("pudgeland.plugin.animal")
client.plugins.load_folder("pudgeland.plugin.economics")
client.plugins.load_folder("pudgeland.plugin.server")

gateway_bot.run()
