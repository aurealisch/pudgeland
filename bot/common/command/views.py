import typing

import miru
import miru.abc

from .error.handler import handlers


class View(miru.View):
    @typing.final
    async def on_error(
        self,
        error: Exception,
        _: typing.Optional[miru.abc.item.ViewItem] = None,
        context: typing.Optional[miru.context.view.ViewContext] = None,
    ) -> None:
        await handlers.ErrorHandler.handle(error, context=context)
