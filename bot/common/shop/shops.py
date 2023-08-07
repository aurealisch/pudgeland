import typing

import msgspec


class Bonus(msgspec.Struct):
    banana: float = 0.0
    monkey: float = 0.0


class Item(msgspec.Struct):
    label: str
    description: str
    emoji: str
    price: int
    bonus: Bonus


with open("./resource/json/shops.json", encoding="utf-8") as stream:
    buf = stream.read()

shop = msgspec.json.decode(buf, type=typing.Mapping[str, Item])
