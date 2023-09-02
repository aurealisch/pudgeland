import os

import dotenv

import prisma as _prisma
from bot import bots, economics
from bot.common import configurations, models
from bot.common.utility.enum.emoji import emojis

dotenv.load_dotenv()

token = os.environ.get("TOKEN")

bot = bots.Bot(
    token,
    model=models.Model(
        economics.Economics(
            economics.Configuration(
                [
                    economics.Event(
                        "Осень",
                        description=f"""\
                            Я календарь переверну - и снова третье сентября..

                            {emojis.Emoji.berry} Множитель сбора ягод: `2,5x`
                            {emojis.Emoji.fox} Множитель сбора ягод лисами: `1,25x`
                        """,
                        buff=economics.Buff(
                            2.5,
                            fox=1.25,
                        ),
                    ),
                ],
            ),
            prisma=_prisma.Prisma(),
        ),
        configuration=configurations.Configuration(
            configurations.Activity("гг сервер умер"),
            leaders=configurations.Leaders(
                configurations.Sort("desc"),
                take=5,
            ),
            plugins=configurations.Plugins(
                configurations.Collect(
                    configurations.Range(
                        75,
                        b=200,
                    ),
                    foxying=configurations.Range(50, b=135.0),
                ),
                cull=configurations.Cull(
                    2,
                    fraction=0.4,
                ),
                tame=configurations.Tame(
                    2,
                    price=250,
                ),
            ),
        ),
    ),
)

_prisma.register(bot.economics.prisma)

if os.name != "nt":
    import uvloop

    uvloop.install()

bot.run()
