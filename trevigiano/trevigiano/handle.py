import traceback

import miru

from trevigiano import contexts, embed


async def handle(exception: Exception,
                 context: contexts.Context | miru.Context) -> None:
    value = exception
    tb = exception.__traceback__

    traceback.print_exception(
        exception.__class__,
        value=value,
        tb=tb,
    )

    await context.respond(
        embed=embed.embed('error', description=f'```{exception}```'))
