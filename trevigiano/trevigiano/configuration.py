import typing

import prisma as _prisma
from trevigiano import types


class Leaders(typing.TypedDict):
    sortOrder: _prisma.types.SortOrder
    take: int


class Range(typing.TypedDict):
    start: types.FloatOrInt
    stop: types.FloatOrInt


class Collect(typing.TypedDict):
    berry: Range
    fox: Range


class Steal(typing.TypedDict):
    probability: types.FloatOrInt
    fraction: types.FloatOrInt


class Tame(typing.TypedDict):
    probability: types.FloatOrInt
    price: types.FloatOrInt


class Plugins(typing.TypedDict):
    collect: Collect
    steal: Steal
    tame: Tame


class Configuration(typing.TypedDict):
    leaders: Leaders
    plugins: Plugins
