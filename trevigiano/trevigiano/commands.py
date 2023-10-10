import datetime
import time
import typing

import crescent
import crescent.ext.cooldowns
import crescent.internal

from trevigiano import (
    contexts,
    embed,
    handle,
    trim,
)


class Command:

    async def callback(self, context: contexts.Context) -> None:
        try:
            await self.call(context)
        except Exception as exception:
            await handle.handle(exception, context=context)

    async def call(self, context: contexts.Context) -> None:
        ...


async def callback(context: crescent.Context,
                   period: datetime.timedelta) -> crescent.HookResult | None:
    timestamp = f'<t:{round(period.total_seconds() + time.time())}:R>'

    description = trim.trim(f"""
        Ты слишком часто используешь эту команду!

        Попробуйте еще раз {timestamp}
    """)

    await context.respond(embed=embed.embed('default', description=description)
                          )

    return crescent.HookResult(True)


def command(
    name: str,
    description: str,
    period: datetime.timedelta,
    group: crescent.Group | None = None
) -> typing.Callable[
    [Command], crescent.internal.Includable[crescent.internal.AppCommandMeta]]:

    def inner(
        command: Command
    ) -> crescent.internal.Includable[crescent.internal.AppCommandMeta]:
        includable = crescent.hook(
            crescent.ext.cooldowns.cooldown(
                1,
                period=period,
                callback=callback,
            ))(crescent.command(
                command,
                name=name,
                description=description,
            ))

        if group is not None:
            includable = group.child(includable)

        return includable

    return inner
