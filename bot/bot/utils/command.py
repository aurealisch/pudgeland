import typing
from datetime import timedelta as datetime_timedelta
from textwrap import dedent as textwrap_dedent
from time import time as time_time

import crescent
from crescent import internal as crescent_internal
from crescent.ext.cooldowns import cooldown as crescent_cooldown

from bot.utils.embed import embed
from bot.utils.handle import handle


class Command:
    async def callback(self, context: crescent.Context) -> None:
        await context.defer()

        try:
            await self.run(context)
        except Exception as exception:
            await handle(context, exception=exception)

    async def run(self, context: crescent.Context) -> None:
        ...


async def callback(
    context: crescent.Context, timedelta: datetime_timedelta
) -> crescent.HookResult | None:
    await context.respond(
        embed=embed(
            "default",
            desc=textwrap_dedent(
                f"""
                    Ты слишком часто используешь эту команду!

                    Попробуйте еще раз <t:{round(timedelta.total_seconds() + time_time())}:R>
                """
            ),
        )
    )

    return crescent.HookResult(True)


def command(
    name: str,
    description: str,
    group: typing.Optional[crescent.Group] = None,
    sub_group: typing.Optional[crescent.SubGroup] = None,
) -> typing.Callable[
    [Command], crescent_internal.Includable[crescent_internal.AppCommandMeta]
]:
    def inner(
        command: Command
    ) -> crescent_internal.Includable[crescent_internal.AppCommandMeta]:
        includable = crescent.hook(
            crescent_cooldown(
                1, period=datetime_timedelta(seconds=10), callback=callback
            )
        )(crescent.command(command, name=name, description=description))

        if group is not None:
            includable = group.child(includable)

        if sub_group is not None:
            includable = sub_group.child(includable)

        return includable

    return inner
