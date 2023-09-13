import typing

import hikari

from .. import economics as _economics
from . import configurations


@typing.final
class Model:
  def __init__(
    self: typing.Self,
    economics: '_economics.Economics',
    configuration: 'configurations.Configuration',
  ) -> None:
    self.economics = economics
    self.configuration = configuration

  async def _on_started_event(
    self: typing.Self,
    _started_event: 'hikari.StartedEvent',
  ) -> None:
    await self.economics.prisma.connect()

  async def _on_stopped_event(
    self: typing.Self,
    _stopped_event: 'hikari.StoppedEvent',
  ) -> None:
    await self.economics.prisma.disconnect()
