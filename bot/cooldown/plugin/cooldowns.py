import string
import time as _time
import typing

import crescent

from bot.locale import locales

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
            # Return the current time in seconds since the Epoch.
            current = _time.time()

        tokens = self._tokens

        if current > self._window + self.period:
            tokens = self.capacity

        return tokens

    @property
    def remained(self) -> float:
        # Return the current time in seconds since the Epoch.
        current = _time.time()

        tokens = self.get_tokens(current)

        if tokens == 0:
            return self.period - (current - self._window)

        return 0.0

    def trigger(self) -> float | None:
        # Return the current time in seconds since the Epoch.
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

        # Return the current time in seconds since the Epoch.
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

    def remained(self, key: _K) -> float:
        return self.get_bucket(key).remained

    def trigger(self, key: _K) -> float | None:
        return self.get_bucket(key).trigger()


def cooldown(
    capacity: float, period: float
) -> typing.Callable[[crescent.Context], typing.Awaitable[crescent.HookResult | None]]:
    _cooldown = Cooldown(capacity, period=period)

    async def inner(context: crescent.Context) -> crescent.HookResult | None:
        remained = _cooldown.trigger(context.user.id)

        if remained is None:
            return None

        locale = context.locale

        # Return the current time in seconds since the Epoch.
        current = _time.time()

        timestamp = f"<t:{int(round(current + remained))}:R>"

        template = string.Template(
            f"""\
                $youUseThisCommandTooOften!

                $tryAgain {timestamp}
            """
        )

        # Respond to an interaction.
        await context.respond(
            locales.of(
                locale,
                locale_builder=locales.LocaleBuilder(
                    f"""\
                        You use this command too often!

                        Try again {timestamp}
                    """,
                    ru=template.substitute(
                        dict(
                            youUseThisCommandTooOften=(
                                "Ты слишком часто используешь эту команду"
                            ),
                            tryAgain="Попробуйте еще раз",
                        ),
                    ),
                    uk=template.substitute(
                        dict(
                            youUseThisCommandTooOften=(
                                "Ти занадто часто використовуєш цю команду"
                            ),
                            tryAgain="Спробуйте ще раз",
                        ),
                    ),
                ),
            ),
        )

        return crescent.HookResult(exit=True)

    return inner


# MIT License
#
# Copyright (c) 2023 elaresai
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in all
# copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.
