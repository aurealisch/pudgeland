import abc
import typing

import miru
import miru.abc

from ..utility import handles


class ViewABC(miru.View, abc.ABC):
  @typing.final
  async def on_error(
    self: typing.Self,
    exception: Exception,
    _: typing.Optional['miru.abc.ViewItem'] = None,
    context: typing.Optional['miru.ViewContext'] = None,
  ) -> None:
    await handles.handle(
      exception,
      context=context,
    )
