import typing
import attrs

from bot.locale.plugin import locales


_ID = typing.TypeVar("_ID")


@attrs.define
class Item:
    name: str | locales.LocaleBuilder
    description: str | locales.LocaleBuilder

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
            description=locales.LocaleBuilder(
                (
                    "Releases a hook that attracts +5% bananas instead of the next"
                    " SFA on the MFA!"
                ),
                ru=(
                    "Выпускает крюк, который вместо очередного СФа на мид"
                    " притягивает +5% бананов!"
                ),
                uk=(
                    "Випускає гак, який замість чергового СФа на мид притягує +5%"
                    " бананів!"
                ),
            ),
            price=500,
        ),
        2: Item(
            locales.LocaleBuilder(
                "The Lost Axe Of The Administrator",
                ru="Затерянный Топор Администратора",
                uk="Загублена Сокира Адміністратора",
            ),
            description=locales.LocaleBuilder(
                (
                    "The admin's lost axe allows you to completely set the tree,"
                    " which gives +10% bananas!"
                ),
                ru=(
                    "Затерянный топор админа позволяет полностью сетнуть дерево,"
                    " что дает +10% бананов!"
                ),
                uk=(
                    "Загублена сокира адміна дозволяє повністю нарікати дерево,"
                    " що дає + 10% бананів!"
                ),
            ),
            price=1000,
        ),
    }
)
