import typing

import crescent


class Command(typing.Protocol):
    async def callback(self, context: crescent.Context) -> None:
        ...
