import time as _time
import typing

import crescent
import hikari

from trevigiano import contexts


class Cooldown:
    def __init__(self, period: int) -> None:
        self.period = period

        self.starts_at: typing.Mapping[hikari.Snowflakeish, float] = {}
        self.ends_at: typing.Mapping[hikari.Snowflakeish, float] = {}

    def remained(self, snowflakeish: hikari.Snowflakeish) -> float | None:
        time = _time.time()

        # fmt: off
        if (
            snowflakeish in self.starts_at
            or snowflakeish in self.ends_at
        ):
            self.starts_at[snowflakeish] = time

            ends_at = self.ends_at[snowflakeish]
            starts_at = self.starts_at[snowflakeish]

            if ends_at <= starts_at:
                del self.ends_at[snowflakeish]
                del self.starts_at[snowflakeish]

                return None

            return (
                self.ends_at[snowflakeish]
                - self.starts_at[snowflakeish]
            )
        # fmt: on

        self.starts_at[snowflakeish] = time
        self.ends_at[snowflakeish] = time + self.period

        return None


def cooldown(
        period: int) -> typing.Callable[[contexts.Context], crescent.HookResult | None]:
    cooldown = Cooldown(period)

    async def inner(context: contexts.Context) -> crescent.HookResult | None:
        embed = context.embed
        trim = context.trim

        remained = cooldown.remained(context.user.id)

        if remained is None:
            return None

        timestamp = f'<t:{round(remained + _time.time())}:R>'

        description = trim.trim(
            f"""
                Ты слишком часто используешь эту команду!

                Попробуйте еще раз {timestamp}
            """
        )

        await context.respond(embed=embed.embed('default', description=description))

        return crescent.HookResult(True)

    return inner
