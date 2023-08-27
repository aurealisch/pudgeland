import crescent
import hikari

from . import models

Plugin = crescent.Plugin[hikari.GatewayBot, models.Model]
