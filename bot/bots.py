import typing

import crescent
import hikari
import miru

from .common import models


@typing.final
class Bot:
  def __init__(
    self: typing.Self,
    plugins: typing.Iterable[str],
    model: 'models.Model',
    token: str,
  ) -> None:
    self.model = model

    intents = (
      hikari.Intents.MESSAGE_CONTENT
      | hikari.Intents.GUILDS
      | hikari.Intents.GUILD_MESSAGES
    )

    gateway_bot = hikari.GatewayBot(token, intents=intents)

    miru.install(gateway_bot)

    client = crescent.Client(gateway_bot, model=model)

    for plugin in plugins:
      client.plugins.load(f'plugin.{plugin}')

    gateway_bot.listen(hikari.StartedEvent)(model._on_started_event)
    gateway_bot.listen(hikari.StoppedEvent)(model._on_stopped_event)

    self.__gateway_bot = gateway_bot

  def run(self: typing.Self) -> None:
    return self.__gateway_bot.run(
      activity=hikari.Activity(name=self.model.configuration.activity.name)
    )
