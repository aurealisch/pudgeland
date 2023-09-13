import os

import env

import prisma as _prisma
from bot import bots, economics
from bot.common import configurations, models
from bot.common.utility import emojis

token = env.get("TOKEN")

# fmt: off
events = [economics.Event(
    "Осень",
    description=f"""\
        {emojis.Emoji.berry} Множитель сбора ягод: `1.1x`
        {emojis.Emoji.fox} Множитель сбора ягод лисами: `1.01x`
    """,
    buff=economics.Buff(
        1.1,
        fox=1.01,
    ),
)]
# fmt: on

configuration = configurations.Configuration(
    configurations.Activity("гг сервер умер"),
    leaders=configurations.Leaders(
        configurations.Sort("desc"),
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

bot = bots.Bot(
    token,
    model=models.Model(
        economics.Economics(
            _prisma.Prisma(),
            events=events,
        ),
        configuration=configuration,
    ),
)

_prisma.register(bot.economics.prisma)

if os.name != "nt":
    import uvloop

    uvloop.install()

bot.run()
