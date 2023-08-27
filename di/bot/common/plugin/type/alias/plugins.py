import crescent
import hikari

from di.bot.common.model.models import Model

Plugin = crescent.Plugin[
  hikari.GatewayBot,
  Model,
]
