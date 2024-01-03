from env import get as env_get

from bot.bot import Bot
from bot.modules.database import Database
from bot.modules.model import Model

Bot(
    [
        "leaders.banana",
        "leaders.monkey",
        "leaders.coin",
        "leaders.diamond",
        "leaders.netherite",
        "purchase.coin",
        "purchase.diamond",
        "purchase.netherite",
        "sale.coin",
        "sale.diamond",
        "sale.netherite",
        "collecting",
        "domestication",
        "profile",
    ],
    model=Model(
        {
            "collecting_range_start": 1,
            "collecting_range_stop": 5,
            "domestication_ratio": 275,
            "purchase_coin": 125,
            "purchase_diamond": 4,
            "purchase_netherite": 8,
        },
        database=Database(
            env_get("HOST"),
            port=env_get("PORT"),
            user=env_get("USER"),
            password=env_get("PASSWORD"),
            database=env_get("DATABASE"),
        ),
    ),
    token=env_get("TOKEN"),
).run()
