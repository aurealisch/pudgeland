import hikari
import crescent

from pudgeland.model import models


class Plugin(crescent.Plugin[hikari.GatewayBot, models.Model]):
    pass
