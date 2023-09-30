import env

import prisma as _prisma
from trevigiano import trevigiano
from trevigiano.client import models
from trevigiano.client.command.utility import emojis
from trevigiano.module import configurations, databases

COMMANDS = [
    "events",
    "profile",
    "berries.collect",
    #  'berries.give',
    "berries.steal",
    "foxes.tame",
    "leaders.berries",
    "leaders.foxes",
    "leaders.reputation",
    "reputation.downgrade",
    "reputation.upgrade",
    "store.items",
    "store.buy",
]
PLUGINS = [f"command.{COMMAND}" for COMMAND in COMMANDS]

PRISMA = _prisma.Prisma()

_prisma.register(PRISMA)

EVENTS = [
    databases.Event(
        "Осень",
        description=f"""\
            {emojis.Emoji.BERRY} Множитель сбора ягод: `1.1x`
            {emojis.Emoji.FOX} Множитель сбора ягод лисами: `1.01x`
        """,
        buff=databases.Buff(1.1, fox=1.01),
    )
]

DATABASE = databases.Database(PRISMA, events=EVENTS)

CONFIGURATION = configurations.of(
    """\
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
    """
)

MODEL = models.Model(CONFIGURATION, database=DATABASE)

TOKEN = env.get("TOKEN")

trevigiano.Trevigiano(
    PLUGINS,
    model=MODEL,
    token=TOKEN,
).run()
