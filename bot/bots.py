import typing

import crescent
import hikari
import miru

from .common import models


class Bot:
  def __init__(
    self: typing.Self,
    token: str,
    model: models.Model,
  ) -> None:
    self.model = model

    self.configuration = self.model.configuration
    self.economics = self.model.economics

    intents = (
      hikari.Intents.MESSAGE_CONTENT
      | hikari.Intents.GUILDS
      | hikari.Intents.GUILD_MESSAGES
    )

    self.gateway_bot = hikari.GatewayBot(
      token,
      intents=intents,
    )

    miru.install(self.gateway_bot)

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

    self.client.plugins.load_folder('bot.plugin')

  def run(self: typing.Self) -> None:
    return self.gateway_bot.run(
      activity=hikari.Activity(
        name=self.configuration.activity.name
      )
    )
