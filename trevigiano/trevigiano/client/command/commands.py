import typing

import crescent

from .. import plugins
from ..error.handler import handles
from . import (
    contexts,
    coolDowns,
    options,
)


def command(
    plugin: "plugins.Plugin",
    name: str,
    description: str,
    period: "coolDowns.Period",
    group: typing.Optional["crescent.Group"] = None,
    options: typing.Optional[typing.Sequence["options.Option"]] = None,
) -> typing.Callable[[crescent.CommandCallbackT], None]:
    def inner(command_callback_t: crescent.CommandCallbackT) -> None:
        async def callback(self: typing.Self, context: "contexts.Context") -> None:
            ARGUMENTS = (context,)

            if context.options:
                for _, VALUE in context.options.items():
                    ARGUMENTS += (VALUE,)

            await context.defer()

            try:
                await command_callback_t(*ARGUMENTS)
            except Exception as exception:
                await handles.handle(exception, context=context)

        NAME = "ClassCommandProto"
        BASES = (crescent.ClassCommandProto,)
        DICT = {"callback": callback}

        if options:
            for option in options:
                DICT[option.name] = crescent.option(
                    option.type,
                    name=option.name,
                    description=option.description,
                )

        TYPE = type(
            NAME,
            BASES,
            DICT,
        )

        hook = crescent.hook(coolDowns.coolDown(period))

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
