import attrs
import crescent

from ..utilities.plugins import plugins


@attrs.define
class Component:
    plugin: plugins.Plugin

    async def callback(self, context: crescent.Context) -> None:
        raise NotImplementedError("Method or function hasn't been implemented yet.")
