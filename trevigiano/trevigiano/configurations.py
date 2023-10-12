import typing


class Range(typing.TypedDict):
    start: float | int
    stop: float | int


class Collect(typing.TypedDict):
    range: Range


class Steal(typing.TypedDict):
    probability: float | int
    fraction: float | int


class Tame(typing.TypedDict):
    probability: float | int
    price: float | int


class Plugins(typing.TypedDict):
    collect: Collect
    steal: Steal
    tame: Tame


class Configuration(typing.TypedDict):
    plugins: Plugins
