import typing


class Range(typing.TypedDict):
    start: typing.Union[float, int]
    stop: typing.Union[float, int]


class Collect(typing.TypedDict):
    range: Range


class Steal(typing.TypedDict):
    probability: typing.Union[float, int]
    fraction: typing.Union[float, int]


class Tame(typing.TypedDict):
    multiplicateur: typing.Union[float, int]


class Plugins(typing.TypedDict):
    collect: Collect
    steal: Steal
    tame: Tame


class Configuration(typing.TypedDict):
    plugins: Plugins
