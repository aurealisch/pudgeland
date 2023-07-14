import threading

import crescent
import hikari
import uvicorn

import prisma

from .api.app import apps
from .database import databases
from .environment import environments
from .model import models

bot = hikari.GatewayBot(environments.gateway_bot_token)

model = models.Model(databases.Database(prisma.Prisma()))

prisma.register(model.database.prisma)

bot.subscribe(hikari.StartedEvent, model.on_started_event)
bot.subscribe(hikari.StoppedEvent, model.on_stopped_event)

client = crescent.Client(bot, model=model)

client.plugins.load_folder("pudgeland.plugin.action")
client.plugins.load_folder("pudgeland.plugin.animal")
client.plugins.load_folder("pudgeland.plugin.economics")
client.plugins.load_folder("pudgeland.plugin.server")

threading.Thread(
    target=lambda: uvicorn.run(
        apps.app,
        host=environments.api_host,
        port=environments.api_port,
    )
).start()

bot.run()
