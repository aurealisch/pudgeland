import typing

import miru
import miru.abc

from trevigiano import handle


class View(miru.View):
    @typing.final
    async def on_error(
        self,
        exception: Exception,
        _viewItem: miru.abc.ViewItem | None = None,
        context: miru.Context | None = None,
    ) -> typing.Awaitable[None]:
        await handle.handle(exception, context=context)
