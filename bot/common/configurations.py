import dataclasses


@dataclasses.dataclass
class Sort:
  order: str


@dataclasses.dataclass
class Leaders:
  sort: Sort
  take: int


@dataclasses.dataclass
class Range:
  a: int
  b: int


@dataclasses.dataclass
class Collect:
  berrying: Range
  foxying: Range


@dataclasses.dataclass
class Cull:
  edge: int
  fraction: float


@dataclasses.dataclass
class Tame:
  edge: int
  price: int


@dataclasses.dataclass
class Plugins:
  collect: Collect
  cull: Cull
  tame: Tame


@dataclasses.dataclass
class Activity:
  name: str


@dataclasses.dataclass
class Configuration:
  activity: Activity
  leaders: Leaders
  plugins: Plugins
