import threading

import crescent
import hikari
import uvicorn

import prisma

from .api.apps import app
from .databases import database
from .environments import environment
from .models import model

bot = hikari.GatewayBot(environment.gateway_bot_token)

model = model.Model(database.Database(prisma.Prisma()))

prisma.register(model.database.prisma)

bot.subscribe(hikari.StartedEvent, model.on_started_event)
bot.subscribe(hikari.StoppedEvent, model.on_stopped_event)

client = crescent.Client(bot, model=model)

client.plugins.load_folder("pudgeland.plugins")

threading.Thread(
    target=lambda: uvicorn.run(
        app.app,
        host=environment.api_host,
        port=environment.api_port,
    )
).start()

bot.run()
