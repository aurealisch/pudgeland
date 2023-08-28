import typing

import crescent
import hikari

from .common.model import models
from .dto.environment import environments


class Bot:
  def __init__(
    self: typing.Self,
    environment: environments.EnvironmentDTO,
    model: models.Model,
  ) -> None:
    token = environment.token

    self.model = model

    self.configuration = self.model.configuration
    self.database = self.model.database

    # intents = (
    #   hikari.Intents.MESSAGE_CONTENT
    #   | hikari.Intents.GUILDS
    #   | hikari.Intents.GUILD_MESSAGES
    # )

    self.gateway_bot = hikari.GatewayBot(
      token,
    #   intents=intents,
    )

    self.gateway_bot.subscribe(
      hikari.StartedEvent,
      callback=self.model.on_started_event,
    )
    self.gateway_bot.subscribe(
      hikari.StoppedEvent,
      callback=self.model.on_stopped_event,
    )

    self.client = crescent.Client(
      self.gateway_bot,
      model=self.model,
    )

    self.client.plugins.load_folder('di.bot.plugin')

  def run(self: typing.Self) -> None:
    return self.gateway_bot.run(
      activity=hikari.Activity(
        name=self.configuration.activity.name
      )
    )
