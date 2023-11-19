import traceback

import crescent

from bot import embed, err


async def handle(ctx: crescent.Context, exception: Exception) -> None:
    val = exception
    tb = exception.__traceback__

    if isinstance(exception, err.Error):
        await ctx.respond(embed=embed.embed("err", desc=f"```{exception}```"))

        return

    traceback.print_exception(exception.__class__, value=val, tb=tb)
