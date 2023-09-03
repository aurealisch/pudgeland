import abc
import typing

import crescent

from .. import contexts
from ..error.handler import handlers


class CommandABC(crescent.ClassCommandProto, abc.ABC):
    async def run(self, context: contexts.Context) -> None:
        raise NotImplementedError

    @typing.final
    async def callback(self, context: contexts.Context) -> None:
        try:
            await self.run(context)
        except Exception as error:
            await handlers.ErrorHandler.handle(error, context=context)
