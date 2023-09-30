import traceback
import typing

import miru

from trevigiano.client.command import contexts
from trevigiano.client.command.utility import embeds


async def handle(
    exception: Exception,
    context: typing.Union["contexts.Context", "miru.Context"],
) -> None:
    VALUE = exception
    TB = exception.__traceback__

    traceback.print_exception(
        exception.__class__,
        value=VALUE,
        tb=TB,
    )

    await context.respond(embed=embeds.embed("error", description=f"```{exception}```"))
