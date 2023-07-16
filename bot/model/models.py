import attrs
import hikari

from bot.common.database import databases


@attrs.define
class Model:
    database: databases.Database

    async def on_started_event(self, _: hikari.StartedEvent) -> None:
        await self.database.prisma.connect()

    async def on_stopped_event(self, _: hikari.StoppedEvent) -> None:
        await self.database.prisma.disconnect()
