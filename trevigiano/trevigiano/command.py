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
        options: typing.Sequence[option.Option] | None = None,) -> typing.Callable[
            [crescent.CommandCallbackT],
            crescent.internal.Includable[crescent.internal.AppCommandMeta]]:
    def inner(
            command_callback_t: crescent.CommandCallbackT) -> crescent.internal.Includable[crescent.internal.AppCommandMeta]:
        async def callback(self, context: context.Context) -> None:
            arguments = (context,)

            if context.options:
                for _, value in context.options.items():
                    arguments += (value,)

            await context.defer()

            try:
                await command_callback_t(*arguments)
            except Exception as exception:
                await handle.handle(exception, context=context)

        name = 'ClassCommandProto'
        bases = (crescent.ClassCommandProto,)
        dict_ = {'callback': callback,}

        if options is not None:
            for option in options:
                dict_[option.name] = crescent.option(option.type_,
                                                     name=option.name,
                                                     description=option.description,
                                                     )

        type_ = type(name,
                    bases,
                    dict_,
                    )

        includable = crescent.hook(coolDown.coolDown(period))(
            crescent.command(type_,
                             name=name,
                             description=description,
                             )
        )

        if group is not None:
            includable = group.child(includable)

        return includable

    return inner
