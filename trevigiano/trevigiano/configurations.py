import decimal
import typing


class Range(typing.TypedDict):
    start: decimal.Decimal
    stop: decimal.Decimal


class Collect(typing.TypedDict):
    range: Range


class Steal(typing.TypedDict):
    probability: decimal.Decimal
    fraction: decimal.Decimal


class Tame(typing.TypedDict):
    probability: decimal.Decimal
    price: decimal.Decimal


class Plugins(typing.TypedDict):
    collect: Collect
    steal: Steal
    tame: Tame


class Configuration(typing.TypedDict):
    plugins: Plugins
