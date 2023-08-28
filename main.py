import os

import dotenv

import prisma as _prisma
from di.bot import bots
from di.bot.common.database import databases
from di.bot.common.dto.configuration import configurations
from di.bot.common.model import models
from di.bot.dto.environment import environments

dotenv.load_dotenv()

token = os.environ.get('TOKEN')

bot = bots.Bot(
  environments.EnvironmentDTO(token),
  model=models.Model(
    databases.Database(_prisma.Prisma()),
    configuration=configurations.ConfigurationDTO(
      configurations.ActivityDTO('гг сервер умер'),
      leaders=configurations.LeadersDTO(
        configurations.SortDTO('desc'),
        take=5,
      ),
      plugins=configurations.PluginsDTO(
        configurations.CollectDTO(
          configurations.RangeDTO(75, b=200),
          monkeying=configurations.RangeDTO(50, b=135)
        ),
        cull=configurations.CullDTO(4, fraction=0.4),
        tame=configurations.TameDTO(4, price=500)
      ),
    )
  ),
)

_prisma.register(bot.database.prisma)

bot.run()
