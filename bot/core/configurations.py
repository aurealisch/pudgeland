"""."""

import typing

import msgspec
import hikari


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

  fraction: float
  edge: int


class Tame(msgspec.Struct):
  """."""

  price: int
  edge: int


class Plugins(msgspec.Struct):
  """."""

  collect: Collect
  cull: Cull
  tame: Tame


class Activity(msgspec.Struct):
  """."""

  name: str


class Port(msgspec.Struct):
  """."""

  default: int


class API(msgspec.Struct):
  """."""

  host: str
  port: Port


class Configuration(msgspec.Struct):
  """."""

  plugins: Plugins
  activity: Activity
  api: API
