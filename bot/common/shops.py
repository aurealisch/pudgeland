"""."""

import typing

import msgspec


Velocity = typing.TypeVar(
  'Velocity',
  float,
  int,
)


class Bonus(msgspec.Struct):
  """."""

  x: Velocity = 0
  y: Velocity = 0


class Item(msgspec.Struct):
  """."""

  label: str
  description: str

  emoji: str

  price: int

  bonus: Bonus


shop = {
  1: Item(
    'Hook',
    description='Выпускает Hook, который вместо очередного Shadow Fiend на центре притягивает +10% бананов!',
    emoji='⛓',
    price=500,
    bonus=Bonus(x=0.1),
  ),
  2: Item(
    'Топор Администратора',
    description='Топор Администратора позволяет моментально полностью срубить дерево, что даёт +30% бананов!',
    emoji='🪓',
    price=1_360,
    bonus=Bonus(x=0.3),
  ),
  3: Item(
    'Модные Тапочки',
    description='Модные Тапочки настолько удобные, что они дают +80% к сбору бананов обезьянами!',
    emoji='🥿',
    price=4_700,
    bonus=Bonus(y=0.8),
  ),
  4: Item(
    'Тропический Напиток',
    description='Тропический Напиток настолько вкусный, что даёт +120% к сбору бананов обезьянами!',
    emoji='🍹',
    price=12_775,
    bonus=Bonus(y=1.2),
  ),
}
