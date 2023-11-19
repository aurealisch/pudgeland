import env

from bot import bot, models
from bot import config as _config
from bot import db as _db

plugins = [
    "profile", "domestication.monkeys", "collecting.bananas",
    "leaders.bananas", "leaders.monkeys", "leaders.coins", "leaders.diamonds",
    "leaders.netherite.scraps", "purchase.coins", "purchase.diamonds",
    "purchase.netherite.scraps", "sale.coins", "sale.diamonds",
    "sale.netherite.scraps"
]

db = _db.Database(env.get("HOST"),
                  port=env.get("PORT"),
                  user=env.get("USER"),
                  password=env.get("PASSWORD"),
                  db=env.get("DB"))

config: _config.Configuration = {
    "plugins": {
        "collect": {
            "rng": {
                "start": 5,
                "stop": 50
            }
        },
        "ratio": {
            "purchase": {
                "coins": 125,
                "diamonds": 4,
                "netherite": {
                    "scraps": 8
                }
            },
            "tame": 250
        }
    }
}

model = models.Model(config, db=db)

token = env.get("TOKEN")

bot.Bot(plugins, model=model, token=token).run()
