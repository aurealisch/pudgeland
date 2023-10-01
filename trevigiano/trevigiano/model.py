import typing

import hikari

from . import configuration, database


class Model:
    def __init__(
        self: typing.Self,
        configuration: "configuration.Configuration",
        database: "database.Database",
    ) -> None:
        self.configuration = configuration
        self.database = database

    async def on_started_event(
        self: typing.Self, _started_event: "hikari.StartedEvent"
    ) -> None:
        await self.database.prisma.connect()

    async def on_stopped_event(
        self: typing.Self, _stopped_event: "hikari.StoppedEvent"
    ) -> None:
        await self.database.prisma.disconnect()
