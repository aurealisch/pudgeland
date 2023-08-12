import os

import crescent
import dotenv
import hikari
import miru
import msgspec

import prisma as _prisma

from ..core.configuration import configurations
from ..core.database import databases
from ..core.environment import environments
from .model import models

dotenv.load_dotenv()

with open("./deprecated/bot/configuration.json") as stream:
    buffer = stream.read()

    configuration = msgspec.json.decode(buffer, type=configurations.Configuration)

prisma = _prisma.Prisma()

_prisma.register(prisma)

database = databases.Database(prisma)

token = os.environ.get("TOKEN")
url = os.environ.get("URL")

default = configuration.api.port.default

port = int(os.environ.get("PORT", default=default))

environment = environments.Environment(token, url=url, port=port)

banner = "bot"

bot = hikari.GatewayBot(environment.token, banner=banner)

miru.install(bot)

model = models.Model(configuration, database=database, environment=environment)

bot.subscribe(hikari.StartedEvent, callback=model.on_started_event)
bot.subscribe(hikari.StoppedEvent, callback=model.on_stopped_event)

client = crescent.Client(bot, model=model)
