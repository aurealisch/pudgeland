import time
import typing

import crescent
import crescent.ext.cooldowns
import crescent.internal

from bot import embed, handle, trim, types


class Command:
    async def callback(self, ctx: crescent.Context) -> None:
        await ctx.defer()

        try:
            await self.cb(ctx)
        except Exception as exception:
            await handle.handle(ctx, exception=exception)

    async def cb(self, ctx: crescent.Context) -> None:
        ...


async def cb(ctx: crescent.Context, period: types.Period) -> crescent.HookResult | None:
    ts = f"<t:{round(period.total_seconds() + time.time())}:R>"

    desc = trim.trim(
        f"""
        Ты слишком часто используешь эту команду!

        Попробуйте еще раз {ts}
    """
    )

    await ctx.respond(embed=embed.embed("default", desc=desc))

    return crescent.HookResult(True)


def cmd(
    name: str,
    desc: str,
    period: types.Period,
    group: typing.Optional[crescent.Group] = None,
    subGroup: typing.Optional[crescent.SubGroup] = None,
) -> typing.Callable[
    [Command], crescent.internal.Includable[crescent.internal.AppCommandMeta]
]:
    def inner(
        cmd: Command
    ) -> crescent.internal.Includable[crescent.internal.AppCommandMeta]:
        includable = crescent.hook(
            crescent.ext.cooldowns.cooldown(1, period=period, callback=cb)
        )(crescent.command(cmd, name=name, description=desc))

        if group is not None:
            includable = group.child(includable)

        if subGroup is not None:
            includable = subGroup.child(includable)

        return includable

    return inner
