from traceback import print_exception as traceback_print_exception

from crescent import Context as crescent_Context

from bot.modules.error import Error
from bot.utils.embed import embed


async def handle(ctx: crescent_Context, exception: Exception) -> None:
    if isinstance(exception, Error):
        await ctx.respond(embed=embed("error", desc=f"```{exception}```"))

        return

    traceback_print_exception(exception.__class__, exception, exception.__traceback__)
