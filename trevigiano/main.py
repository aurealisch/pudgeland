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

configuration = configurations.Configuration(
  configurations.Activity('гг сервер умер'),
  leaders=configurations.Leaders(
    configurations.Sort('desc'),
    take=5,
  ),
  plugins=configurations.Plugins(
    configurations.Collect(
      configurations.Range(25, b=100),
      foxying=configurations.Range(100, b=250),
    ),
    cull=configurations.Cull(3, fraction=0.1),
    tame=configurations.Tame(5, price=200),
  ),
)

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
