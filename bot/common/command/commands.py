import typing

import crescent
import crescent.internal

from . import contexts, cooldowns
from . import options as _options


def command(
    name: str,
    description: str,
    period: cooldowns.Period,
    group: typing.Optional[crescent.Group] = None,
    options: typing.Optional[typing.Sequence[_options.Option]] = None,
) -> typing.Callable[
    [tuple],
    # fmt: off
    crescent.internal.Includable[
        crescent.internal.AppCommandMeta,
    ]
    # fmt: on
]:
    def inner(*args) -> crescent.internal.Includable[crescent.internal.AppCommandMeta]:
        callback, *_ = args

        async def _callback(self, context: contexts.Context) -> None:
            arguments = (context,)

            if context.options:
                for _, value in context.options.items():
                    arguments += (value,)

            return await callback(*arguments)

        __name = "Command"
        __bases = (object,)
        __dict = {
            "callback": _callback,
        }

        if options:
            for option in options:
                __dict[option.name] = crescent.option(
                    option.type,
                    name=option.name,
                    description=option.description,
                )

        __type = type(
            __name,
            __bases,
            __dict,
        )

        includable = crescent.hook(cooldowns.cooldown(period))(
            crescent.command(
                __type,
                name=name,
                description=description,
            )
        )

        if group:
            includable = group.child(includable)

        return includable

    return inner
