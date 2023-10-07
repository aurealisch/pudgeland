import hikari

from trevigiano import configuration, database


class Model:
    def __init__(
            self,
            configuration: configuration.Configuration,
            database: database.Database) -> None:
        self.configuration = configuration
        self.database = database

    async def on_started_event(self, _started_event: hikari.StartedEvent) -> None:
        await self.database.connect()

    async def on_stopped_event(self, _stopped_event: hikari.StoppedEvent) -> None:
        await self.database.close()
