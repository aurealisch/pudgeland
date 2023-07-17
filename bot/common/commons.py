import hikari

import prisma
from bot.client import clients
from bot.client.model import models
from bot.common.database import databases
from bot.common.environment import environments

bot = hikari.GatewayBot(environments.gateway_bot_token)

database = databases.Database(prisma.Prisma())

prisma.register(database.prisma)

model = models.Model(database)

bot.subscribe(hikari.StartedEvent, model.on_started_event)
bot.subscribe(hikari.StoppedEvent, model.on_stopped_event)

client = clients.Client(bot, model=model)
