"""."""

import msgspec


class Activity(msgspec.Struct):
  """."""

  name: str


class Sort(msgspec.Struct):
  """."""

  order: str


class Leaders(msgspec.Struct):
  """."""

  sort: Sort

  take: int


class Range(msgspec.Struct):
  """."""

  a: int
  b: int


class Collect(msgspec.Struct):
  """."""

  collecting: Range
  monkeying: Range


class Cull(msgspec.Struct):
  """."""

  edge: int
  fraction: float


class Tame(msgspec.Struct):
  """."""

  edge: int
  price: int


class Plugins(msgspec.Struct):
  """."""

  collect: Collect
  cull: Cull
  tame: Tame


class Configuration(msgspec.Struct):
  """."""

  activity: Activity
  leaders: Leaders
  plugins: Plugins
