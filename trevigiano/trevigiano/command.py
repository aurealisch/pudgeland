import typing

import crescent

from . import (
    context,
    cool_down,
    handle,
    option,
    plugin,
)


def command(
    plugin: "plugin.Plugin",
    name: str,
    description: str,
    period: "cool_down.Period",
    group: typing.Optional["crescent.Group"] = None,
    options: typing.Optional[typing.Sequence["option.Option"]] = None,
) -> typing.Callable[[crescent.CommandCallbackT], None]:
    def inner(command_callback_t: crescent.CommandCallbackT) -> None:
        async def callback(self: typing.Self, context: "context.Context") -> None:
            ARGUMENTS = (context,)

            if context.options:
                for _, VALUE in context.options.items():
                    ARGUMENTS += (VALUE,)

            await context.defer()

            try:
                await command_callback_t(*ARGUMENTS)
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

        hook = crescent.hook(cool_down.cool_down(period))

        includable = hook(
            crescent.command(
                TYPE,
                name=name,
                description=description,
            )
        )

        if group:
            includable = group.child(includable)

        plugin.include(includable)

    return inner
