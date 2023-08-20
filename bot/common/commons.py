"""."""

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

with open(
  './configuration.json',
  encoding='utf-8',
) as stream:
  buf = stream.read()

  type__ = configurations.Configuration

  configuration = msgspec.json.decode(
    buf,
    type=type__,
  )

prisma = _prisma.Prisma()

_prisma.register(prisma)

database = databases.Database(prisma)

token = os.environ.get('TOKEN')

environment = environments.Environment(token)

model = models.Model(
  configuration,
  database=database,
  environment=environment,
)

bot = hikari.GatewayBot(model.environment.token)

miru.install(bot)

bot.subscribe(
  hikari.StartedEvent,
  callback=model.on_started_event,
)
bot.subscribe(
  hikari.StoppedEvent,
  callback=model.on_stopped_event,
)

client = crescent.Client(
  bot,
  model=model,
)
