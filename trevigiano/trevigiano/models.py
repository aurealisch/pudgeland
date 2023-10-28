from trevigiano import configurations, databases

import hikari


class Model:

    def __init__(self, configuration: configurations.Configuration,
                 database: databases.Database) -> None:
        """Description"""
        self.configuration = configuration
        self.database = database

    async def onStartedEvent(self, _: hikari.StartedEvent) -> None:
        """Description"""
        await self.database.connect()

    async def onStoppedEvent(self, _: hikari.StoppedEvent) -> None:
        """Description"""
        await self.database.close()
