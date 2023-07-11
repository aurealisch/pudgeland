import attrs
import hikari
import collei

from ..database import databases


@attrs.define
class Model:
    client: collei.Client
    database: databases.Database

    async def on_started_event(self, _: hikari.StartedEvent) -> None:
        pass

    async def on_stopped_event(self, _: hikari.StoppedEvent) -> None:
        pass
