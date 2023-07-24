import string

import crescent
import hikari
import miru

from bot.cooldown.plugin import cooldowns
from bot.locale import locales
from bot.plugin import _plugins
from bot.plugin.economy.shop import _shops

plugin = _plugins.Plugin()

# 5 seconds
period = 5


class View(miru.View):
    # A decorator to transform a coroutine function into a Discord UI Button's callback.
    # This must be inside a subclass of View.
    @miru.button(label="ОК", style=hikari.ButtonStyle.SECONDARY, emoji="✅")
    async def ok(self, _: miru.Button, view_context: miru.ViewContext) -> None:
        pass

    # A decorator to transform a coroutine function into a Discord UI Button's callback.
    # This must be inside a subclass of View.
    @miru.button(label="Отменить", style=hikari.ButtonStyle.SECONDARY, emoji="❌")
    async def cancel(self, _: miru.Button, view_context: miru.ViewContext) -> None:
        locale = view_context.locale

        view = view_context.view

        title = locales.of(
            locale,
            locale_builder=locales.LocaleBuilder(
                "Cancel",
                ru="Отменить",
                uk="Відмінивши",
            ),
        )

        description = locales.of(
            locale,
            locale_builder=locales.LocaleBuilder(
                "Cancelled",
                ru="Отменено",
                uk="Скасований",
            ),
        )

        embed = hikari.Embed(title=title, description=description)

        # Short-hand method to create a new message response via the interaction this
        # context represents.
        await view_context.respond(embed=embed, flags=hikari.MessageFlag.EPHEMERAL)

        if view is not None:
            # Stop listening for interactions.
            view.stop()


@plugin.include
# Register a hook to a command.
@crescent.hook(cooldowns.cooldown(1, period=period))
# Register a slash command.
@crescent.command(
    name=locales.LocaleBuilder(
        "buy",
        ru="купить",
        uk="купити",
    ),
    description=locales.LocaleBuilder(
        "Buy",
        ru="Купить",
        uk="Купити",
    ),
)
class Buy:
    # An option when declaring a command using class syntax.
    item = crescent.option(
        int,
        name=locales.LocaleBuilder(
            "item",
            ru="предмет",
            uk="предмет",
        ),
        description=locales.LocaleBuilder(
            "Item",
            ru="Предмет",
            uk="Предмет",
        ),
        choices=[(item.name, id__) for id__, item in _shops.shop.items()],
    )

    # noinspection PyMethodMayBeStatic
    async def callback(self, context: crescent.Context) -> None:
        locale = context.locale

        item = _shops.shop.get(self.item)

        price = item.price

        view = View(timeout=60)

        title = locales.of(
            locale,
            locale_builder=locales.LocaleBuilder(
                "Buy",
                ru="Купить",
                uk="Купити",
            ),
        )

        template = string.Template(
            f"$to_buy_this_item_you_will_need `{price}` $bananas"
        )

        description = locales.of(
            locale,
            locale_builder=locales.LocaleBuilder(
                f"To buy this item you will need `{price}` bananas",
                ru=template.substitute(
                    dict(
                        to_buy_this_item_you_will_need=(
                            "Чтобы купить этот предмет потребуется"
                        ),
                        bananas="бананов",
                    ),
                ),
                uk=template.substitute(
                    dict(
                        to_buy_this_item_you_will_need=(
                            "Щоб купити цей предмет потрібно"
                        ),
                        bananas="бананів",
                    ),
                ),
            ),
        )

        embed = hikari.Embed(title=title, description=description)

        # Respond to an interaction.
        message = await context.respond(
            ensure_message=True,
            ephemeral=True,
            components=view,
            embed=embed,
        )

        if message is not None:
            # Start up the view and begin listening for interactions.
            await view.start(message)


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
