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
  bananing: RangeDTO
  monkeying: RangeDTO


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
class ActivityDTO:
  name: str


@dataclasses.dataclass
class ConfigurationDTO:
  activity: ActivityDTO
  leaders: LeadersDTO
  plugins: PluginsDTO
