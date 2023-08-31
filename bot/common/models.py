import typing

import hikari

from .. import economics as _economics
from . import configurations


class Model:
  def __init__(
    self: typing.Self,
    economics: _economics.Economics,
    configuration: configurations.Configuration
  ) -> None:
    self.economics = economics
    self.configuration = configuration

  async def on_started_event(
    self: typing.Self,
    _: hikari.StartedEvent
  ) -> None:
    return await self.economics.prisma.connect()

  async def on_stopped_event(
    self: typing.Self,
    _: hikari.StoppedEvent
  ) -> None:
    return await self.economics.prisma.disconnect()
