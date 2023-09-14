import env

import prisma as _prisma
from bot import bots, economics
from bot.common import configurations, models
from bot.common.utility import emojis

commands = [
  'events',
  'profile',

  'berries.collect',
  'berries.cull',
  #  'berries.give',

  'foxes.tame',

  'leaders.berries',
  'leaders.foxes',
  'leaders.reputation',

  'reputation.downgrade',
  'reputation.upgrade',

  'store.items',
  'store.purchase',
]
plugins = [f'command.{command}' for command in commands]

events = [economics.Event(
  'Осень',
  description=f"""\
    {emojis.Emoji.berry} Множитель сбора ягод: `1.1x`
    {emojis.Emoji.fox} Множитель сбора ягод лисами: `1.01x`
  """,
  buff=economics.Buff(
    1.1,
    fox=1.01,
  ),
)]

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
    "cull": {"probability": 3, "fraction": 0.1},
    "tame": {"probability": 5, "price": 200}
  }
}
""")

token = env.get('TOKEN')

bot = bots.Bot(
  plugins,
  model=models.Model(
    economics.Economics(
      _prisma.Prisma(),
      events=events,
    ),
    configuration=configuration,
  ),
  token=token,
)

_prisma.register(bot.model.economics.prisma)

bot.run()
