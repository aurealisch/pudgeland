import attrs
import crescent


@attrs.define
class Component:
    async def callback(self, context: crescent.Context) -> None:
        raise NotImplementedError("Method or function hasn't been implemented yet.")
