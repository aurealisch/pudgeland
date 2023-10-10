import traceback

import flare

from trevigiano import contexts, embed


async def handle(
        exception: Exception,
        contextOrMessageContext: contexts.Context | flare.MessageContext
) -> None:
    value = exception
    tb = exception.__traceback__

    traceback.print_exception(
        exception.__class__,
        value=value,
        tb=tb,
    )

    await contextOrMessageContext.respond(
        embed=embed.embed('error', description=f'```{exception}```'))
