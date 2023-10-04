import typing

import crescent
import crescent.internal

from trevigiano import (
    context,
    coolDown,
    handle,
    option,
)


def command(
    name: str,
    description: str,
    period: int,
    group: crescent.Group | None = None,
    options: typing.Sequence[option.Option] | None = None,
) -> typing.Callable[
    [crescent.CommandCallbackT],
    crescent.internal.Includable[crescent.internal.AppCommandMeta],
]:
    def inner(
        commandCallbackT: crescent.CommandCallbackT,
    ) -> crescent.internal.Includable[crescent.internal.AppCommandMeta]:
        async def callback(self, context: context.Context) -> None:
            ARGUMENTS = (context,)

            if context.options:
                for _, VALUE in context.options.items():
                    ARGUMENTS += (VALUE,)

            await context.defer()

            try:
                await commandCallbackT(*ARGUMENTS)
            except Exception as exception:
                await handle.handle(exception, context=context)

        NAME = "ClassCommandProto"
        BASES = (crescent.ClassCommandProto,)
        DICT = {"callback": callback}

        if options:
            for OPTION in options:
                DICT[OPTION.name] = crescent.option(
                    OPTION.type__,
                    name=OPTION.name,
                    description=OPTION.description,
                )

        TYPE = type(
            NAME,
            BASES,
            DICT,
        )

        includable = crescent.hook(coolDown.coolDown(period))(
            crescent.command(
                TYPE,
                name=name,
                description=description,
            )
        )

        if group:
            includable = group.child(includable)

        return includable

    return inner
