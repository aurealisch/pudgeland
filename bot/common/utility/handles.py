import traceback

from ..command import contexts


async def handle(
    exception: Exception,
    context: "contexts.Context",
) -> None:
    value = exception
    tb = exception.__traceback__

    traceback.print_exception(
        exception.__class__,
        value=value,
        tb=tb,
    )

    # fmt: off
    await context.respond(embed=context.embed(
        "error",
        description=f"```{exception}```",
    ))
    # fmt: on
