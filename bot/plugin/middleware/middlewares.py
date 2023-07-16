import attrs
import crescent

from bot.plugin import plugins


@attrs.define
class Middleware:
    plugin: plugins.Plugin

    async def callback(self, context: crescent.Context) -> None:
        raise NotImplementedError("Method or function hasn't been implemented yet.")
