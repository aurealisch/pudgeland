import hikari

from bot.modules.configuration import Configuration
from bot.modules.database import Database
from bot.modules.emoji import Emoji


class Model:
    def __init__(self, configuration: Configuration, database: Database, emoji: Emoji) -> None:
        self.configuration = configuration
        self.database = database
        self.emoji = emoji

    async def on_started_event(self, _: hikari.StartedEvent) -> None:
        await self.database.connect()

    async def on_stopped_event(self, _: hikari.StoppedEvent) -> None:
        await self.database.close()
