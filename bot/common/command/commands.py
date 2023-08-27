import typing

import crescent

from .error.handler import handlers


class Command:
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
    except Exception as error: # pylint: disable=broad-exception-caught
      await handlers.ErrorHandler.handle(
        error,
        context=context,
      )
