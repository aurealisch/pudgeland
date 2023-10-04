import typing

from trevigiano import types


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
    plugins: Plugins
