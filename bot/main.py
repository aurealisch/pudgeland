from env import get as env_get

from bot.bot import Bot
from bot.modules.configuration import Configuration
from bot.modules.database import Database
from bot.modules.model import Model

Bot(
    Model(
        Configuration(
            1,
            collecting_range_stop=5,
            domestication_ratio=500,
            purchase_coin_ratio=250,
            purchase_diamond_ratio=4,
            purchase_netherite_ratio=8,
        ),
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
