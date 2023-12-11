import env

from bot import bot, models
from bot import config as _config
from bot import db as _db

cmds = [
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
]

db = _db.Database(
    env.get("HOST"),
    port=env.get("PORT"),
    user=env.get("USER"),
    password=env.get("PASSWORD"),
    db=env.get("DB"),
)

config: _config.Configuration = {
    "collectingRngStart": 5,
    "collectingRngStop": 50,
    "domesticationRatio": 275,
    "purchaseCoin": 125,
    "purchaseDiamond": 4,
    "purchaseNetherite": 8,
}

model = models.Model(config, db=db)

token = env.get("TOKEN")

bot.Bot(cmds, model=model, token=token).run()
