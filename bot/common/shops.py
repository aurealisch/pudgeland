import dataclasses
import typing

Velocity = typing.TypeVar(
  'Velocity',
  float,
  int,
)


@dataclasses.dataclass
class Bonus:
  berry: Velocity = 0
  fox: Velocity = 0


@dataclasses.dataclass
class Item:
  label: str
  description: str
  emoji: str
  price: int
  bonus: Bonus


shop = {
  1: Item(
    'Hook',
    description='Выпускает Hook, который вместо очередного Shadow Fiend на центре притягивает +10% ягод!',
    emoji='⛓',
    price=500,
    bonus=Bonus(berry=0.1),
  ),
  2: Item(
    'Топор Администратора',
    description='Топор Администратора позволяет моментально полностью срубить дерево, что даёт +30% ягод!',
    emoji='🪓',
    price=1_360,
    bonus=Bonus(berry=0.3),
  ),
  3: Item(
    'Модные Тапочки',
    description='Модные Тапочки настолько удобные, что они дают +80% к сбору ягод лисами!',
    emoji='🥿',
    price=4_700,
    bonus=Bonus(fox=0.8),
  ),
  4: Item(
    'Тропический Напиток',
    description='Тропический Напиток настолько вкусный, что даёт +120% к сбору ягод лисами!',
    emoji='🍹',
    price=12_775,
    bonus=Bonus(fox=1.2),
  ),
}
