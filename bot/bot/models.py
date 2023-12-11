import hikari

from bot import config as _config
from bot import db as _db


class Model:
    def __init__(self, config: _config.Configuration, db: _db.Database) -> None:
        self.config = config
        self.db = db

    async def onStartedE(self, _: hikari.StartedEvent) -> None:
        await self.db.connect()

    async def onStoppedE(self, _: hikari.StoppedEvent) -> None:
        await self.db.close()
