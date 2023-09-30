import env

import prisma as _prisma
from trevigiano import trevigiano
from trevigiano.client import model
from trevigiano.modules import configuration, database

COMMANDS = [
    "profile",
    "berries.collect",
    #  "berries.give",
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
PLUGINS = [f"commands.{COMMAND}" for COMMAND in COMMANDS]

PRISMA = _prisma.Prisma()

_prisma.register(PRISMA)

DATABASE = database.Database(PRISMA)

CONFIGURATION = configuration.of(
    """\
    {
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

MODEL = model.Model(CONFIGURATION, database=DATABASE)

TOKEN = env.get("TOKEN")

trevigiano.Trevigiano(
    PLUGINS,
    model=MODEL,
    token=TOKEN,
).run()
