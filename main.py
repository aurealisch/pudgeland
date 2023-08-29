import os

import dotenv

import prisma as _prisma
from bot import bots
from bot.common import (
  configurations,
  databases,
  models,
)

dotenv.load_dotenv()

token = os.environ.get('TOKEN')

bot = bots.Bot(
  token,
  model=models.Model(
    databases.Database(_prisma.Prisma()),
    configuration=configurations.Configuration(
      configurations.Activity('гг сервер умер'),
      leaders=configurations.Leaders(
        configurations.Sort('desc'),
        take=5,
      ),
      plugins=configurations.Plugins(
        configurations.Collect(
          configurations.Range(75, b=200),
          monkeying=configurations.Range(50, b=135)
        ),
        cull=configurations.Cull(4, fraction=0.4),
        tame=configurations.Tame(4, price=500)
      ),
    )
  ),
)

_prisma.register(bot.database.prisma)

bot.run()
