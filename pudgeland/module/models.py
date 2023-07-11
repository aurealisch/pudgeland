import attrs
import hikari

from ..database import databases


@attrs.define
class Model:
    database: databases.Database

    async def on_started_event(self, _: hikari.StartedEvent) -> None:
        pass

    async def on_stopped_event(self, _: hikari.StoppedEvent) -> None:
        pass
