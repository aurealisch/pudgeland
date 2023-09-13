import crescent
import hikari

from bot.common import models

from .abc import views
from .command import (
  commands,
  contexts,
  cooldowns,
  exceptions,
  options,
)


class Plugin(crescent.Plugin[
  hikari.GatewayBot,
  models.Model,
]):
  views = views
  commands = commands
  contexts = contexts
  cooldowns = cooldowns
  exceptions = exceptions
  options = options
