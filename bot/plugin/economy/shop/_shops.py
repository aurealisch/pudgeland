import string
import typing
import attrs

from bot.locale.plugin import locales


_ID = typing.TypeVar("_ID")


@attrs.define
class Item:
    name: str | locales.LocaleBuilder
    description: str

    price: int


@attrs.define
class Shop:
    items: typing.Mapping[_ID, Item]


shop = Shop(
    {
        1: Item(
            locales.LocaleBuilder(
                "Hook",
                ru="Крюк",
                uk="Гак",
            ),
            description=string.whitespace.join(
                (
                    "Выпускает крюк, который вместо очередного СФа на миде притягивает",
                    "+5% бананов!",
                )
            ),
            price=500,
        ),
        2: Item(
            locales.LocaleBuilder(
                "The Lost Axe Of The Administrator",
                ru="Затерянный Топор Администратора",
                uk="Загублена Сокира Адміністратора",
            ),
            description=string.whitespace.join(
                (
                    "Затерянный топор админа позволяет полностью сетнуть дерево, что"
                    "дает +10% бананов!"
                )
            ),
            price=1000,
        ),
    }
)
