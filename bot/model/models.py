import attrs
import hikari


from ..databases import database


@attrs.define
class Model:
    database: database.Database

    async def on_started_event(self, _: hikari.StartedEvent) -> None:
        await self.database.prisma.connect()

    async def on_stopped_event(self, _: hikari.StoppedEvent) -> None:
        await self.database.prisma.disconnect()
