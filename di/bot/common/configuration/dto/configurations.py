import dataclasses


@dataclasses.dataclass
class SortDTO:
  order: str


@dataclasses.dataclass
class LeadersDTO:
  sort: SortDTO
  take: int


@dataclasses.dataclass
class RangeDTO:
  a: int
  b: int


@dataclasses.dataclass
class CollectDTO:
  xing: RangeDTO
  ying: RangeDTO


@dataclasses.dataclass
class CullDTO:
  edge: int
  fraction: float


@dataclasses.dataclass
class TameDTO:
  edge: int
  price: int


@dataclasses.dataclass
class PluginsDTO:
  collect: CollectDTO
  cull: CullDTO
  tame: TameDTO


@dataclasses.dataclass
class BunchesDTO:
  x: str
  y: str


@dataclasses.dataclass
class EmojisDTO:
  x: str
  y: str


@dataclasses.dataclass
class ActivityDTO:
  name: str


@dataclasses.dataclass
class ConfigurationDTO:
  activity: ActivityDTO
  leaders: LeadersDTO
  plugins: PluginsDTO
  bunches: BunchesDTO
  emojis: EmojisDTO
