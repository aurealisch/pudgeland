import hikari

from bot.modules.configuration import Configuration
from bot.modules.database import Database


class Model:
    def __init__(self, configuration: Configuration, database: Database) -> None:
        self.configuration = configuration
        self.database = database

    async def on_started_event(self, _: hikari.StartedEvent) -> None:
        await self.database.connect()

    async def on_stopped_event(self, _: hikari.StoppedEvent) -> None:
        await self.database.close()
