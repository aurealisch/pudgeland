import env

from trevigiano import (
    configuration,
    database,
    environment,
    model,
    trevigiano,
)

COMMANDS = [
    "profile",
    "berries.collect",
    "berries.steal",
    "foxes.tame",
    "leaders.berries",
    "leaders.foxes",
    "leaders.reputation",
    "reputation.downgrade",
    "reputation.upgrade",
]
PLUGINS = [f"commands.{COMMAND}" for COMMAND in COMMANDS]

DATABASE = database.Database()

CONFIGURATION: configuration.Configuration = {
    "leaders": {"sortOrder": "desc", "take": 6},
    "plugins": {
        "collect": {
            "berry": {"start": 100, "stop": 250},
            "fox": {"start": 25, "stop": 100}
        },
        "steal": {"fraction": 0.1, "probability": 3},
        "tame": {"price": 100, "probability": 5}
    }
}

ENVIRONMENT = environment.Environment(
    env.get("HOST"),
    port=env.get("PORT"),
    user=env.get("USER"),
    password=env.get("PASSWORD"),
    database=env.get("DATABASE"),
)

MODEL = model.Model(
    CONFIGURATION,
    database=DATABASE,
    environment=ENVIRONMENT,
)

TOKEN = env.get("TOKEN")

trevigiano.Trevigiano(
    PLUGINS,
    model=MODEL,
    token=TOKEN,
).run()
