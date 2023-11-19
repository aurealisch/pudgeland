import typing

from bot import types


class Range(typing.TypedDict):
    start: types.Start
    stop: types.Stop


class Collect(typing.TypedDict):
    rng: Range


class Netherite(typing.TypedDict):
    scraps: types.Scraps


class Purchase(typing.TypedDict):
    coins: types.Coins
    diamonds: types.Diamonds
    netherite: Netherite


class Ratio(typing.TypedDict):
    tame: types.Tame
    purchase: Purchase


class Plugins(typing.TypedDict):
    collect: Collect
    ratio: Ratio


class Configuration(typing.TypedDict):
    plugins: Plugins
