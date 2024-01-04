from traceback import print_exception as traceback_print_exception

from crescent import Context as crescent_Context

from bot.modules.error import Error
from bot.utilities.embed import embed


async def handle_exception(context: crescent_Context, exception: Exception) -> None:
    if isinstance(exception, Error):
        await context.respond(
            embeds=embed("error", title="error", description=f"```{exception}```")
        )

        return

    traceback_print_exception(exception.__class__, exception, exception.__traceback__)
