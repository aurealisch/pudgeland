"""."""

import typing

import msgspec


class Bonus(msgspec.Struct):
  """."""

  x: float = 0.0
  y: float = 0.0


class Item(msgspec.Struct):
  """."""

  label: str
  description: str

  emoji: str

  price: int

  bonus: Bonus


with open(
  './asset/json/shop/shops.json',
  encoding='utf-8',
) as stream:
  buf = stream.read()

type__ = typing.Mapping[str, Item]

shop = msgspec.json.decode(buf, type=type__)
