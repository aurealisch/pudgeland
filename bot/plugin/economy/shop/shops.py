import string

import crescent
import hikari

from bot.cooldown.plugin import cooldowns
from bot.locale import locales
from bot.plugin import _plugins
from bot.plugin.economy.shop import _shops

plugin = _plugins.Plugin()


# 5 seconds
period = 5


@plugin.include
# Register a hook to a command.
@crescent.hook(cooldowns.cooldown(1, period=period))
# Register a slash command.
@crescent.command(
    name=locales.LocaleBuilder(
        "shop",
        ru="магазин",
        uk="магазин",
    ),
    description=locales.LocaleBuilder(
        "Shop",
        ru="Магазин",
        uk="Магазин",
    ),
)
class Shop:
    # noinspection PyMethodMayBeStatic
    async def callback(self, context: crescent.Context) -> None:
        locale = context.locale

        title = locales.of(
            locale,
            locale_builder=locales.LocaleBuilder(
                "Shop",
                ru="Магазин",
                uk="Магазин",
            ),
        )

        description = string.whitespace

        for id__, item in _shops.shop.items.items():
            _name = locales.of(locale, locale_builder=item.name)
            _description = locales.of(locale, locale_builder=item.description)

            template = string.Template(
                f"""
                # {id__}. {_name}

                $price: 🍌 `{item.price}` $bananas

                $description:\n> {_description}
                """
            )

            description += locales.of(
                locale,
                locale_builder=locales.LocaleBuilder(
                    f"""
                        # {id__}. {_name}

                        Price: 🍌 `{item.price}` bananas

                        Description:\n> {_description}
                    """,
                    ru=template.substitute(
                        dict(
                            price="Цена",
                            bananas="бананов",
                            description="Описание",
                        ),
                    ),
                    uk=template.substitute(
                        dict(
                            price="Ціна",
                            bananas="бананів",
                            description="Опис",
                        ),
                    ),
                ),
            )

        embed = hikari.Embed(title=title, description=description)

        # Respond to an interaction.
        await context.respond(embed=embed)


# MIT License
#
# Copyright (c) 2023 pudgeland
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
