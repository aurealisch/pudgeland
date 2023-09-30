import traceback
import typing

import miru

from trevigiano.client.command import contexts
from trevigiano.client.command.utility import embeds


async def handle(
    exception: Exception,
    context: typing.Union[
        "contexts.Context",
        "miru.Context",
    ],
) -> None:
    value = exception
    tb = exception.__traceback__

    traceback.print_exception(
        exception.__class__,
        value=value,
        tb=tb,
    )

    await context.respond(
        embed=embeds.embed(
            "error",
            description=f"```{exception}```",
        )
    )
