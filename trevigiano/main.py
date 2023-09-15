import env

import prisma as _prisma
from trevigiano import trevigiano
from trevigiano.client import models
from trevigiano.client.command.utility import emojis
from trevigiano.module import configurations, databases

commands = [
  'events',
  'profile',

  'berries.collect',
  #  'berries.give',
  'berries.steal',

  'foxes.tame',

  'leaders.berries',
  'leaders.foxes',
  'leaders.reputation',

  'reputation.downgrade',
  'reputation.upgrade',

  'store.items',
  'store.buy',
]
plugins = [f'command.{command}' for command in commands]

prisma = _prisma.Prisma()

_prisma.register(prisma)

events = [databases.Event(
  'Осень',
  description=f"""\
    {emojis.Emoji.berry} Множитель сбора ягод: `1.1x`
    {emojis.Emoji.fox} Множитель сбора ягод лисами: `1.01x`
  """,
  buff=databases.Buff(
    1.1,
    fox=1.01,
  ),
)]

database = databases.Database(
  prisma,
  events=events,
)

configuration = configurations.of("""\
{
  "activity": {
    "name": "гг сервер умер"
  },
  "leaders": {
    "sort": {
      "order": "desc"
    },
    "take": 5
  },
  "plugins": {
    "collect": {
      "berry": {"start": 25, "stop": 100},
      "fox": {"start": 100, "stop": 250}
    },
    "steal": {"probability": 3, "fraction": 0.1},
    "tame": {"probability": 5, "price": 200}
  }
}
""")

model = models.Model(
  configuration,
  database=database,
)

token = env.get('TOKEN')

trevigiano.Trevigiano(
  plugins,
  model=model,
  token=token,
).run()
