import crescent
import hikari

from bot.model import models


class Plugin(crescent.Plugin[hikari.GatewayBot, models.Model]):
    pass
