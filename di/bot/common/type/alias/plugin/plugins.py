import crescent
import hikari

from di.bot.common import models

Plugin = crescent.Plugin[
  hikari.GatewayBot,
  models.Model,
]
