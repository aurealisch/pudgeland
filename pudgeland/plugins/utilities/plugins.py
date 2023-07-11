import hikari
import crescent

from pudgeland.modules import models


class Plugin(crescent.Plugin[hikari.GatewayBot, models.Model]):
    pass
