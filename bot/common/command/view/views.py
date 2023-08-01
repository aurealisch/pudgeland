import miru
import miru.abc


class View(miru.View):
    def on_error(
        self,
        error: Exception,
        _: miru.abc.item.ViewItem | None = None,
        _context: miru.context.view.ViewContext | None = None,
    ) -> None:
        raise error
