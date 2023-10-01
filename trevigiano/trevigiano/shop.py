import dataclasses
import typing

from . import float_or_int


@dataclasses.dataclass
class Bonus:
    berry: typing.Optional["float_or_int.FloatOrInt"] = None
    fox: typing.Optional["float_or_int.FloatOrInt"] = None


@dataclasses.dataclass
class Item:
    label: typing.Optional[str] = None
    description: typing.Optional[str] = None
    emoji: typing.Optional[str] = None
    price: typing.Optional[int] = None
    bonus: typing.Optional[Bonus] = None


shop = {
    1: Item(
        "Hook",
        description="Выпускает Hook, который вместо очередного Shadow Fiend на центре притягивает +10% ягод!",  # noqa: E501
        emoji="⛓",
        price=500,
        bonus=Bonus(berry=0.1),
    ),
    2: Item(
        "Топор Администратора",
        description="Топор Администратора позволяет моментально полностью срубить дерево, что даёт +30% ягод!",  # noqa: E501
        emoji="🪓",
        price=1_360,
        bonus=Bonus(berry=0.3),
    ),
    3: Item(
        "Модные Тапочки",
        description="Модные Тапочки настолько удобные, что они дают +80% к сбору ягод лисами!",  # noqa: E501
        emoji="🥿",
        price=4_700,
        bonus=Bonus(fox=0.8),
    ),
    4: Item(
        "Тропический Напиток",
        description="Тропический Напиток настолько вкусный, что даёт +120% к сбору ягод лисами!",  # noqa: E501
        emoji="🍹",
        price=12_775,
        bonus=Bonus(fox=1.2),
    ),
}
