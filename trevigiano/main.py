import env

from trevigiano import (
    configuration,
    database,
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

DATABASE = database.Database(
    env.get("HOST"),
    port=env.get("PORT"),
    user=env.get("USER"),
    password=env.get("PASSWORD"),
    database=env.get("DATABASE"),
)

CONFIGURATION: configuration.Configuration = {
    "plugins": {
        "collect": {
            "berry": {"start": 100, "stop": 250},
            "fox": {"start": 25, "stop": 100}
        },
        "steal": {"fraction": 0.1, "probability": 3},
        "tame": {"price": 100, "probability": 5}
    }
}

MODEL = model.Model(CONFIGURATION, database=DATABASE)

TOKEN = env.get("TOKEN")

trevigiano.Trevigiano(
    PLUGINS,
    model=MODEL,
    token=TOKEN,
).run()
