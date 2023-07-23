import typing
import attrs

from bot.locale import locales


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
                    "Releases a hook that attracts +5% bananas instead of the next SFA"
                    " in the center!"
                ),
                ru=(
                    "Выпускает крюк, который вместо очередного СФа на центре"
                    " притягивает +5% бананов!"
                ),
                uk=(
                    "Випускає гак, який замість чергового СФа на центрі притягує + 5%"
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

# MIT License
#
# Copyright (c) 2023 elaresai
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in all
# copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.
