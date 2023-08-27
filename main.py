import os

import dotenv
import prisma as _prisma

from di.bot.bots import Bot
from di.bot.common.databases import Database
from di.bot.environment.dto.environments import EnvironmentDTO
from di.bot.common.model.models import Model

dotenv.load_dotenv()

token = os.environ.get('TOKEN')

bot = Bot(
  EnvironmentDTO(token),
  model=Model(Database(_prisma.Prisma())),
)

_prisma.register(bot.database.prisma)

bot.run()
