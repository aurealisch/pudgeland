import hikari
import crescent

from pudgeland.module import models


class Plugin(crescent.Plugin[hikari.GatewayBot, models.Model]):
    pass
