import typing


class Range(typing.TypedDict):
    start: typing.Union[float, int]
    stop: typing.Union[float, int]


class Collect(typing.TypedDict):
    range: Range


class Netherite(typing.TypedDict):
    scraps: typing.Union[float, int]


class Purchase(typing.TypedDict):
    coins: typing.Union[float, int]
    diamonds: typing.Union[float, int]

    netherite: Netherite


class Multipliers(typing.TypedDict):
    tame: typing.Union[float, int]

    purchase: Purchase


class Plugins(typing.TypedDict):
    collect: Collect
    multipliers: Multipliers


class Configuration(typing.TypedDict):
    plugins: Plugins
