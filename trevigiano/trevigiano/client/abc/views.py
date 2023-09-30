import abc
import typing

import miru
import miru.abc

from ..error.handler import handles


class ViewABC(miru.View, abc.ABC):
    @typing.final
    async def on_error(
        self: typing.Self,
        exception: Exception,
        _view_item: typing.Optional["miru.abc.ViewItem"] = None,
        context: typing.Optional["miru.Context"] = None,
    ) -> None:
        await handles.handle(exception, context=context)
