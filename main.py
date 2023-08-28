import os

import dotenv

import prisma as _prisma
from di.bot import bots
from di.bot.common.database import databases
from di.bot.common.model import models
from di.bot.dto.environment import environments

dotenv.load_dotenv()

token = os.environ.get('TOKEN')

bot = bots.Bot(
  environments.EnvironmentDTO(token),
  model=models.Model(databases.Database(_prisma.Prisma())),
)

_prisma.register(bot.database.prisma)

bot.run()
