import hikari

from trevigiano import configuration, database


class Model:
    def __init__(
        self,
        configuration: configuration.Configuration,
        database: database.Database,
    ) -> None:
        self.configuration = configuration
        self.database = database

    async def onStartedEvent(self, _startedEvent: hikari.StartedEvent) -> None:
        await self.database.connect()

    async def onStoppedEvent(self, _stoppedEvent: hikari.StoppedEvent) -> None:
        await self.database.close()
