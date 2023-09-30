import typing

import hikari

from ..module import configurations, databases


class Model:
    def __init__(
        self: typing.Self,
        configuration: "configurations.Configuration",
        database: "databases.Database",
    ) -> None:
        self.configuration = configuration
        self.database = database

    async def _on_started_event(
        self: typing.Self, _started_event: "hikari.StartedEvent"
    ) -> None:
        await self.database.prisma.connect()

    async def _on_stopped_event(
        self: typing.Self, _stopped_event: "hikari.StoppedEvent"
    ) -> None:
        await self.database.prisma.disconnect()
