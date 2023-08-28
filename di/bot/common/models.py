import typing

import hikari

from . import databases
from .dto.configuration import configurations


class Model:
  def __init__(
    self: typing.Self,
    database: databases.Database,
    configuration: configurations.ConfigurationDTO
  ) -> None:
    self.database = database
    self.configuration = configuration

  async def on_started_event(
    self: typing.Self,
    _: hikari.StartedEvent
  ) -> None:
    return await self.database.connect()

  async def on_stopped_event(
    self: typing.Self,
    _: hikari.StoppedEvent
  ) -> None:
    return await self.database.disconnect()
