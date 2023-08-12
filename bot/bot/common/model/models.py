import attrs
import hikari

from bot.core.configuration import configurations
from bot.core.database import databases
from bot.core.environment import environments


@attrs.define
class Model:
    configuration: configurations.Configuration
    database: databases.Database
    environment: environments.Environment

    # noinspection PyMethodMayBeStatic
    async def on_started_event(self, _: hikari.StartedEvent) -> None:
        await self.database.prisma.connect()

    # noinspection PyMethodMayBeStatic
    async def on_stopped_event(self, _: hikari.StoppedEvent) -> None:
        await self.database.prisma.disconnect()
