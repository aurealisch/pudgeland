"""."""

import time as _time
import typing

import attrs
import crescent

_KEY = typing.TypeVar('_KEY')


@attrs.define
class Period:
  """."""

  weeks: float = 0.0
  days: float = 0.0
  hours: float = 0.0
  minutes: float = 0.0
  seconds: float = 0.0
  milliseconds: float = 0.0
  microseconds: float = 0.0

  @property
  def total(self) -> float:
    """."""
    return (
      self.weeks * 7 * 24 * 60 * 60
      + self.days * 24 * 60 * 60
      + self.hours * 60 * 60
      + self.minutes * 60
      + self.seconds
      + self.milliseconds / 1000
      + self.microseconds / 1000000
    )


class SlidingWindow:
  """."""

  def __init__(self, capacity: float, period: float) -> None:
    """."""
    self.capacity: int = int(capacity)
    self.period: float = float(period)
    self._window: float = 0.0
    self._tokens: int = self.capacity
    self._last: float = 0.0

  def get_tokens(self, current: typing.Optional[float] = None) -> int:
    """."""
    if not current:
      current = _time.time()

    tokens = self._tokens

    if current > self._window + self.period:
      tokens = self.capacity

    return tokens

  @property
  def remained(self) -> float:
    """."""
    current = _time.time()

    tokens = self.get_tokens(current)

    if tokens == 0:
      return self.period - (current - self._window)

    return 0.0

  def trigger(self) -> typing.Optional[float]:
    """."""
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
    """."""
    self._tokens = self.capacity
    self._last = 0.0


class Cooldown(typing.Generic[_KEY]):
  """."""

  def __init__(self, capacity: float, period: float) -> None:
    """."""
    self.period = period
    self.capacity = capacity

    self._old: dict[_KEY, SlidingWindow] = {}
    self._current: dict[_KEY, SlidingWindow] = {}

    self.last_cycle = _time.time()

  def __getitem__(self, key: _KEY) -> SlidingWindow:
    """."""
    if value := self._old.pop(key, None):
      self._current[key] = value

    return self._current[key]

  def __setitem__(self, key: _KEY, value: SlidingWindow) -> None:
    """."""
    self._current[key] = value

  def get_bucket(self, key: _KEY) -> SlidingWindow:
    """."""
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

  def remained(self, key: _KEY) -> float:
    """."""
    return self.get_bucket(key).remained

  def trigger(self, key: _KEY) -> typing.Optional[float]:
    """."""
    return self.get_bucket(key).trigger()


def cooldown(
  capacity: float, period: Period
) -> typing.Callable[
  [crescent.Context], typing.Awaitable[typing.Optional[crescent.HookResult]]
]:
  """."""
  total = period.total

  _period = total

  _cooldown = Cooldown(
    capacity,
    period=_period,
  )

  async def inner(context: crescent.Context) -> typing.Optional[crescent.HookResult]:
    """."""
    remained = _cooldown.trigger(context.user.id)

    if remained is None:
      return None

    current = _time.time()

    future = int(round(current + remained))

    timestamp = f'<t:{future}:R>'

    await context.respond(
      f"""\
        Ты слишком часто используешь эту команду!

        Попробуйте еще раз {timestamp}
      """,
      ephemeral=True,
    )

    return crescent.HookResult(True)

  return inner
