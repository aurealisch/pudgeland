import datetime
import time
import typing

import crescent
import crescent.ext.cooldowns
import crescent.internal

from bot import contexts, embed, handle, trim


class Command:

    async def callback(self, context: contexts.Context) -> None:
        """Description"""
        await context.defer()

        try:
            await self.call(context)
        except Exception as exception:
            await handle.handle(context, exception=exception)

    async def call(self, context: contexts.Context) -> None:
        """Description"""
        ...


async def callback(context: crescent.Context,
                   period: datetime.timedelta) -> crescent.HookResult | None:
    """Description"""
    timestamp = f"<t:{round(period.total_seconds() + time.time())}:R>"

    description = trim.trim(f"""
        Ты слишком часто используешь эту команду!

        Попробуйте еще раз {timestamp}
    """)

    await context.respond(embed=embed.embed("default", description=description)
                          )

    return crescent.HookResult(True)


def command(
    name: str,
    description: str,
    period: datetime.timedelta,
    group: typing.Optional[crescent.Group] = None,
    subGroup: typing.Optional[crescent.SubGroup] = None,
) -> typing.Callable[
    [Command], crescent.internal.Includable[crescent.internal.AppCommandMeta]]:
    """Description"""

    def inner(
        command: Command,
    ) -> crescent.internal.Includable[crescent.internal.AppCommandMeta]:
        """Description"""
        includable = crescent.hook(
            crescent.ext.cooldowns.cooldown(
                1, period=period,
                callback=callback))(crescent.command(command,
                                                     name=name,
                                                     description=description))

        if group is not None:
            includable = group.child(includable)

        if subGroup is not None:
            includable = subGroup.child(includable)

        return includable

    return inner
