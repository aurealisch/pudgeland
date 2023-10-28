import traceback
import typing

import flare

from trevigiano import contexts, embed, errors


async def handle(
    contextOrMessageContext: typing.Union["contexts.Context",
                                          flare.MessageContext],
    exception: Exception,
) -> None:
    """Description"""
    value = exception
    tb = exception.__traceback__

    if isinstance(exception, errors.Error):
        await contextOrMessageContext.respond(
            embed=embed.embed("error", description=f"```{exception}```"))

        return

    traceback.print_exception(exception.__class__, value=value, tb=tb)
