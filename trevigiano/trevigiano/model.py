import hikari

from trevigiano import configuration, database, environment


class Model:
    def __init__(
        self,
        configuration: configuration.Configuration,
        database: database.Database,
        environment: environment.Environment,
    ) -> None:
        self.configuration = configuration
        self.database = database
        self.environment = environment

    async def onStartedEvent(self, _startedEvent: hikari.StartedEvent) -> None:
        await self.database.connect(
            self.environment.host,
            port=self.environment.port,
            user=self.environment.user,
            password=self.environment.password,
            database=self.environment.database,
        )

        await self.database.createTableIfNotExists()

    async def onStoppedEvent(self, _stoppedEvent: hikari.StoppedEvent) -> None:
        await self.database.close()
