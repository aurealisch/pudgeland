import msgspec


class Activity(msgspec.Struct):
  name: str


class Sort(msgspec.Struct):
  order: str


class Leaders(msgspec.Struct):
  sort: Sort
  take: int


class Range(msgspec.Struct):
  a: int
  b: int


class Collect(msgspec.Struct):
  xing: Range
  ying: Range


class Cull(msgspec.Struct):
  edge: int
  fraction: float


class Tame(msgspec.Struct):
  edge: int
  price: int


class Plugins(msgspec.Struct):
  collect: Collect
  cull: Cull
  tame: Tame


class Resource(msgspec.Struct):
  bunch: str


X = Resource
Y = Resource


class Economics(msgspec.Struct):
  x: X
  y: Y


class Emojis(msgspec.Struct):
  x: str
  y: str


class Configuration(msgspec.Struct):
  activity: Activity
  leaders: Leaders
  plugins: Plugins
  economics: Economics
  emojis: Emojis
