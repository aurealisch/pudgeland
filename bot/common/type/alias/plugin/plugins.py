import crescent
import hikari

from bot.common import models

Plugin = crescent.Plugin[
  hikari.GatewayBot,
  models.Model,
]
