import dataclasses
import typing


@typing.final
@dataclasses.dataclass
class Sort:
  order: str


@typing.final
@dataclasses.dataclass
class Leaders:
  sort: Sort
  take: int


@typing.final
@dataclasses.dataclass
class Range:
  a: int
  b: int


@typing.final
@dataclasses.dataclass
class Collect:
  berrying: Range
  foxying: Range


@typing.final
@dataclasses.dataclass
class Cull:
  edge: int
  fraction: float


@typing.final
@dataclasses.dataclass
class Tame:
  edge: int
  price: int


@typing.final
@dataclasses.dataclass
class Plugins:
  collect: Collect
  cull: Cull
  tame: Tame


@typing.final
@dataclasses.dataclass
class Activity:
  name: str


@typing.final
@dataclasses.dataclass
class Configuration:
  activity: Activity
  leaders: Leaders
  plugins: Plugins
