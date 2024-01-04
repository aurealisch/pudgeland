from env import get as env_get

from bot.bot import Bot
from bot.modules.configuration import Configuration
from bot.modules.database import Database
from bot.modules.emoji import Emoji
from bot.modules.model import Model

Bot(
    Model(
        Configuration(
            1,
            collecting_range_stop=5,
            domestication_base_cost=500,
            domestication_multiplier=1.15,
            purchase_coin_multiplier=250,
            purchase_diamond_multiplier=4,
            purchase_netherite_multiplier=8,
        ),
        database=Database(
            env_get("HOST"),
            port=env_get("PORT"),
            user=env_get("USER"),
            password=env_get("PASSWORD"),
            database=env_get("DATABASE"),
        ),
        emoji=Emoji(
            "<:E_Banana:1172161691686031430>",
            monkey="<:E_Monkey:1171112299621253208>",
            coin="<:E_Coin:1167478859474685982>",
            diamond="<:E_Diamond:1147867834114904156>",
            netherite="<:E_Netherite:1165365535119249559>",
            leaders_first="<:E_Leaders_First:1157684768075419681>",
            leaders_second="<:E_Leaders_Second:1157684791827759214>",
            leaders_third="<:E_Leaders_Third:1157684793488719932>",
            four="<:E_Four:1183999351236866168>",
            six="<:E_Six:1183999397479059456>",
            eight="<:E_Eight:1184005049022693376>",
            confirmation_ok="<:E_Confirmation_OK:1154061905686708274>",
            confirmation_cancel="<:E_Confirmation_Cancel:1153393415317368883>",
        ),
    ),
    token=env_get("TOKEN"),
).run()
