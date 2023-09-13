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

  async def started(
    self: typing.Self,
    _: 'hikari.StartedEvent',
  ) -> None:
    await self.economics.prisma.connect()

  async def stopped(
    self: typing.Self,
    _: 'hikari.StoppedEvent',
  ) -> None:
    await self.economics.prisma.disconnect()
