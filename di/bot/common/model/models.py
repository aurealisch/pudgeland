import typing

import hikari

from di.bot.common import databases

from .. import commons


class Model:
  def __init__(
    self: typing.Self,
    database: databases.Database,
  ) -> None:
    self.configuration = commons.configuration
    self.database = database

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
