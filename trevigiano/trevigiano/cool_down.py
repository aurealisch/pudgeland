import dataclasses
import time as _time
import typing

import crescent

from trevigiano import float_or_int

from . import context

_KEY = typing.TypeVar("_KEY")


@dataclasses.dataclass
class Period:
    weeks: "float_or_int.FloatOrInt" = 0
    days: "float_or_int.FloatOrInt" = 0
    hours: "float_or_int.FloatOrInt" = 0
    minutes: "float_or_int.FloatOrInt" = 0
    seconds: "float_or_int.FloatOrInt" = 0
    milliseconds: "float_or_int.FloatOrInt" = 0
    microseconds: "float_or_int.FloatOrInt" = 0

    @property
    def total(self: typing.Self) -> "float_or_int.FloatOrInt":
        return (
            self.weeks * 7 * 24 * 60 * 60
            + self.days * 24 * 60 * 60
            + self.hours * 60 * 60
            + self.minutes * 60
            + self.seconds
            + self.milliseconds / 1_000
            + self.microseconds / 1_000_000
        )


class Bucket:
    def __init__(self: typing.Self, capacity: int, total: float) -> None:
        self.capacity = capacity
        self.total = total
        self._window = 0.0
        self._tokens = self.capacity
        self._last = 0.0

    def get_tokens(self: typing.Self, current: typing.Optional[float] = None) -> int:
        if not current:
            current = _time.time()

        tokens = self._tokens

        if current > self._window + self.total:
            tokens = self.capacity

        return tokens

    @property
    def remained(self: typing.Self) -> float:
        current = _time.time()

        tokens = self.get_tokens(current)

        if tokens == 0:
            return self.total - (current - self._window)

        return 0.0

    def trigger(self: typing.Self) -> typing.Optional[float]:
        current = _time.time()

        self._last = current

        self._tokens = self.get_tokens(current)

        if self._tokens == self.capacity:
            self._window = current

        if self._tokens == 0:
            return self.total - (current - self._window)

        self._tokens -= 1

        return None

    def reset(self: typing.Self) -> None:
        self._tokens = self.capacity
        self._last = 0.0


class CoolDown(typing.Generic[_KEY]):
    def __init__(self: typing.Self, capacity: float, total: float) -> None:
        self.total = total
        self.capacity = capacity

        self._old: dict[_KEY, Bucket] = {}
        self._current: dict[_KEY, Bucket] = {}

        self.last_cycle = _time.time()

    def __getitem__(self: typing.Self, key: _KEY) -> Bucket:
        if value := self._old.pop(key, None):
            self._current[key] = value

        return self._current[key]

    def __setitem__(self: typing.Self, key: _KEY, value: Bucket) -> None:
        self._current[key] = value

    def get_bucket(self: typing.Self, key: _KEY) -> Bucket:
        now = _time.time()

        if now > self.last_cycle + self.total:
            self.last_cycle = now

            self._old.clear()

            currrent = self._current
            self._current = self._old
            self._old = currrent

        try:
            return self[key]
        except KeyError:
            bucket = Bucket(self.capacity, self.total)

            self._current[key] = bucket

            return bucket

    def remained(self: typing.Self, key: _KEY) -> float:
        return self.get_bucket(key).remained

    def trigger(self: typing.Self, key: _KEY) -> typing.Optional[float]:
        return self.get_bucket(key).trigger()


def cool_down(
    period: Period,
) -> typing.Callable[
    ["context.Context"], typing.Awaitable[typing.Optional[crescent.HookResult]]
]:
    async def inner(
        context: "context.Context",
    ) -> typing.Optional[crescent.HookResult]:
        remained = CoolDown(1, total=period.total).trigger(context.user.id)

        if remained is None:
            return None

        current = _time.time()

        future = round(current + remained)

        timestamp = f"<t:{future}:R>"

        await context.respond(
            embed=context.embeds.embed(
                "default",
                description=f"""\
                    Ты слишком часто используешь эту команду!

                    Попробуйте еще раз {timestamp}
                """,
            )
        )

        return crescent.HookResult(True)

    return inner
