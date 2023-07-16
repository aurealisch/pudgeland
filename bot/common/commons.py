import crescent
import hikari

import prisma
from bot.common.database import databases
from bot.common.environment import environments
from bot.model import models

bot = hikari.GatewayBot(environments.gateway_bot_token)

model = models.Model(databases.Database(prisma.Prisma()))

prisma.register(models.database.prisma)

bot.subscribe(hikari.StartedEvent, model.on_started_event)
bot.subscribe(hikari.StoppedEvent, model.on_stopped_event)

client = crescent.Client(bot, model=model)
