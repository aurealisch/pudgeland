import typing

import msgspec

from .. import types


class Activity(msgspec.Struct):
    name: str


class Sort(msgspec.Struct):
    order: typing.Literal["asc", "desc"]


class Leaders(msgspec.Struct):
    sort: Sort
    take: int


class Range(msgspec.Struct):
    start: "types.FloatOrInt"
    stop: "types.FloatOrInt"


class Collect(msgspec.Struct):
    berry: Range
    fox: Range


class Steal(msgspec.Struct):
    probability: "types.FloatOrInt"
    fraction: "types.FloatOrInt"


class Tame(msgspec.Struct):
    probability: "types.FloatOrInt"
    price: "types.FloatOrInt"


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
