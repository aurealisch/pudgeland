import traceback
import typing

import miru

from trevigiano import context, embed


async def handle(
    exception: Exception,
    context: typing.Union["context.Context", "miru.Context"],
) -> None:
    VALUE = exception
    TB = exception.__traceback__

    traceback.print_exception(
        exception.__class__,
        value=VALUE,
        tb=TB,
    )

    await context.respond(embed=embed.embed("error", description=f"```{exception}```"))
