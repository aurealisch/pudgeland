import dataclasses
import typing

Velocity = typing.TypeVar(
  'Velocity',
  float,
  int,
)


@dataclasses.dataclass
class BonusDTO:
  x: Velocity = 0
  y: Velocity = 0


@dataclasses.dataclass
class ItemDTO:
  label: str
  description: str

  emoji: str

  price: int

  bonus: BonusDTO


shop = {
  1: ItemDTO(
    'Hook',
    description='Выпускает Hook, который вместо очередного Shadow Fiend на центре притягивает +10% бананов!',
    emoji='⛓',
    price=500,
    bonus=BonusDTO(x=0.1),
  ),
  2: ItemDTO(
    'Топор Администратора',
    description='Топор Администратора позволяет моментально полностью срубить дерево, что даёт +30% бананов!',
    emoji='🪓',
    price=1_360,
    bonus=BonusDTO(x=0.3),
  ),
  3: ItemDTO(
    'Модные Тапочки',
    description='Модные Тапочки настолько удобные, что они дают +80% к сбору бананов обезьянами!',
    emoji='🥿',
    price=4_700,
    bonus=BonusDTO(y=0.8),
  ),
  4: ItemDTO(
    'Тропический Напиток',
    description='Тропический Напиток настолько вкусный, что даёт +120% к сбору бананов обезьянами!',
    emoji='🍹',
    price=12_775,
    bonus=BonusDTO(y=1.2),
  ),
}
