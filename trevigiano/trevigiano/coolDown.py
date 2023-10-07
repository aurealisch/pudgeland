import time as _time
import typing

import crescent
import hikari

from trevigiano import context


class CoolDown:
    def __init__(self, period: int) -> None:
        self.period = period

        self.startsAt: typing.Mapping[hikari.Snowflakeish, float] = {}
        self.endsAt: typing.Mapping[hikari.Snowflakeish, float] = {}

    def remained(self, snowflakeish: hikari.Snowflakeish) -> float | None:
        TIME = _time.time()

        # fmt: off
        if (
            snowflakeish in self.startsAt
            or snowflakeish in self.endsAt
        ):
            self.startsAt[snowflakeish] = TIME

            endsAt = self.endsAt[snowflakeish]
            startsAt = self.startsAt[snowflakeish]

            if endsAt <= startsAt:
                del self.endsAt[snowflakeish]
                del self.startsAt[snowflakeish]

                return None

            return (
                self.endsAt[snowflakeish]
                - self.startsAt[snowflakeish]
            )
        # fmt: on

        self.startsAt[snowflakeish] = TIME
        self.endsAt[snowflakeish] = TIME + self.period

        return None


def coolDown(
    period: int,
) -> typing.Callable[[context.Context], crescent.HookResult | None]:
    coolDown = CoolDown(period)

    async def inner(context: context.Context) -> crescent.HookResult | None:
        EMBED = context.embed
        TRIM = context.trim

        remained = coolDown.remained(context.user.id)

        if remained is None:
            return None

        timestamp = f"<t:{round(remained + _time.time())}:R>"

        await context.respond(
            embed=EMBED.embed(
                "default",
                description=TRIM.trim(
                    f"""\
                        Ты слишком часто используешь эту команду!

                        Попробуйте еще раз {timestamp}
                    """
                ),
            )
        )

        return crescent.HookResult(True)

    return inner
