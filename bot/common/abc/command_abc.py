import abc
import typing

import crescent

from ..error.handler import handlers


class CommandABC(abc.ABC):
  async def run(
    self: typing.Self,
    context: crescent.Context,
  ) -> None:
    raise NotImplementedError

  @typing.final
  async def callback(
    self: typing.Self,
    context: crescent.Context,
  ) -> None:
    try:
      await self.run(context)
    except Exception as error:
      await handlers.ErrorHandler.handle(
        error,
        context=context,
      )
