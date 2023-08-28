import crescent
import hikari

from di.bot.common.model import models

Plugin = crescent.Plugin[
  hikari.GatewayBot,
  models.Model,
]
