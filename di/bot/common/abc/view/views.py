import abc
import typing

import miru
import miru.abc

from di.bot.common.error.handler import handlers


class ViewABC(miru.View, abc.ABC):
  @typing.final
  async def on_error(
    self: typing.Self,
    error: Exception,
    _: typing.Optional[miru.abc.item.ViewItem] = None,
    context: typing.Optional[miru.context.view.ViewContext] = None,
  ) -> None:
    await handlers.ErrorHandler.handle(
      error,
      context=context,
    )
