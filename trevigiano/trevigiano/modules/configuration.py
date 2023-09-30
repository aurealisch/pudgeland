import typing

import msgspec

from .. import float_or_int


class Activity(msgspec.Struct):
    name: str


class Sort(msgspec.Struct):
    order: typing.Literal["asc", "desc"]


class Leaders(msgspec.Struct):
    sort: Sort
    take: int


class Range(msgspec.Struct):
    start: "float_or_int.FloatOrInt"
    stop: "float_or_int.FloatOrInt"


class Collect(msgspec.Struct):
    berry: Range
    fox: Range


class Steal(msgspec.Struct):
    probability: "float_or_int.FloatOrInt"
    fraction: "float_or_int.FloatOrInt"


class Tame(msgspec.Struct):
    probability: "float_or_int.FloatOrInt"
    price: "float_or_int.FloatOrInt"


class Plugins(msgspec.Struct):
    collect: Collect
    steal: Steal
    tame: Tame


class Configuration(msgspec.Struct):
    activity: Activity
    leaders: Leaders
    plugins: Plugins


def of(buf: typing.Union[bytes, str]) -> Configuration:
    return msgspec.json.decode(buf, type=Configuration)
