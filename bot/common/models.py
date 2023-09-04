import typing

import hikari

from .. import economics as _economics
from . import configurations


@typing.final
class Model:
    def __init__(
        self,
        economics: _economics.Economics,
        configuration: configurations.Configuration,
    ) -> None:
        self.economics = economics
        self.configuration = configuration

    async def started(
        self,
        _: hikari.StartedEvent,
    ) -> None:
        return await self.economics.prisma.connect()

    async def stopped(
        self,
        _: hikari.StoppedEvent,
    ) -> None:
        return await self.economics.prisma.disconnect()
