import time as _time
import typing

import crescent

_K = typing.TypeVar("_K")


class SlidingWindow:
    def __init__(self, capacity: float, period: float) -> None:
        self.capacity: int = int(capacity)
        self.period: float = float(period)
        self._window: float = 0.0
        self._tokens: int = self.capacity
        self._last: float = 0.0

    def get_tokens(self, current: float | None = None) -> int:
        if not current:
            current = _time.time()

        tokens = self._tokens

        if current > self._window + self.period:
            tokens = self.capacity

        return tokens

    @property
    def remained(self) -> float:
        current = _time.time()
        tokens = self.get_tokens(current)

        if tokens == 0:
            return self.period - (current - self._window)

        return 0.0

    def trigger(self) -> float | None:
        current = _time.time()
        self._last = current

        self._tokens = self.get_tokens(current)

        if self._tokens == self.capacity:
            self._window = current

        if self._tokens == 0:
            return self.period - (current - self._window)

        self._tokens -= 1

        return None

    def reset(self) -> None:
        self._tokens = self.capacity
        self._last = 0.0


class Cooldown(typing.Generic[_K]):
    def __init__(self, capacity: float, period: float) -> None:
        self.period = period
        self.capacity = capacity

        self._old: dict[_K, SlidingWindow] = {}
        self._current: dict[_K, SlidingWindow] = {}

        self.last_cycle = _time.time()

    def __getitem__(self, key: _K) -> SlidingWindow:
        if v := self._old.pop(key, None):
            self._current[key] = v

        return self._current[key]

    def __setitem__(self, key: _K, value: SlidingWindow) -> None:
        self._current[key] = value

    def get_bucket(self, key: _K) -> SlidingWindow:
        now = _time.time()

        if now > self.last_cycle + self.period:
            self.last_cycle = now

            self._old.clear()

            currrent = self._current
            self._current = self._old
            self._old = currrent

        try:
            return self[key]
        except KeyError:
            sliding_windows = SlidingWindow(self.capacity, self.period)

            self._current[key] = sliding_windows

            return sliding_windows

    @property
    def remained(self, key: _K) -> float:
        return self.get_bucket(key).remained

    def trigger(self, key: _K) -> float | None:
        return self.get_bucket(key).trigger()


def cooldown(capacity: float, period: float) -> None:
    cooldown = Cooldown(capacity, period=period)

    async def inner(context: crescent.Context) -> None:
        remained = cooldown.trigger(context.user.id)

        if remained is None:
            return None

        now = _time.time()

        timestamp = f"<t:{int(round(now + remained))}:R>"

        await context.respond(
            f"""\
                Ты слишком часто используешь эту команду!

                Попробуйте еще раз {timestamp}
            """
        )

        return crescent.HookResult(exit=True)

    return inner
