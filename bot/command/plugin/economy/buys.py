import datetime

import crescent
import hikari
import miru

from bot.command import cooldowns, exceptions
from bot.command.plugin import _plugins
from bot.shop import items, shops
from bot.utility import embeds

# TODO: Use `hikari-flare` instead of `hikari-miru`

plugin = _plugins.Plugin()

period = cooldowns.Period(seconds=5)


class View(miru.View):
    def __init__(
        self,
        item_id: items.Id,
        *,
        timeout: float | int | datetime.timedelta | None = 120,
        autodefer: bool = True,
    ) -> None:
        self.item_id = item_id

        super().__init__(timeout=timeout, autodefer=autodefer)

    # A decorator to transform a coroutine function into a Discord UI Button's callback.
    @miru.button(label="ОК", style=hikari.ButtonStyle.SECONDARY, emoji="✅")
    async def ok(self, _: miru.Button, view_context: miru.ViewContext) -> None:
        view = view_context.view

        # Short-hand method to defer an interaction response.
        await view_context.defer(flags=hikari.MessageFlag.EPHEMERAL)

        _contextish = str(view_context.user.id)

        contextish = await plugin.model.database.find_first(_contextish)

        banana = contextish.banana
        monkey = contextish.monkey
        reputation = contextish.reputation
        item = contextish.item

        if int(self.item_id) == item:
            raise ValueError

        # Return the value for key if key is in the dictionary, else default.
        item = shops.shop.get(self.item_id)

        price = item.price
        name = item.name

        if price > banana:
            raise exceptions.NotEnoughBanana

        banana -= price

        await plugin.model.database.middleware.update(
            _contextish,
            banana=banana,
            monkey=monkey,
            reputation=reputation,
            item=int(self.itemId),
        )

        title = "Купить"
        description = f"""\
            <@{_contextish}> купил `{name}` за `{price}` бананов

            ```diff\n- {price} бананов 🍌```
            ```diff\n+ {name}```
        """

        embed = embeds.embed("default", title=title, description=description)

        # Short-hand method to create a new message response via the interaction
        # this context represents.
        await view_context.respond(embed=embed)

        if view is not None:
            # Stop listening for interactions.
            view.stop()

    # A decorator to transform a coroutine function into a Discord UI Button's callback.
    # This must be inside a subclass of View.
    @miru.button(label="Отменить", style=hikari.ButtonStyle.SECONDARY, emoji="❌")
    async def cancel(self, _: miru.Button, view_context: miru.ViewContext) -> None:
        view = view_context.view

        title = "Отменить"
        description = "Отменено"

        embed = embeds.embed("default", title=title, description=description)

        # Short-hand method to create a new message response via the interaction
        # this context represents.
        await view_context.respond(embed=embed, flags=hikari.MessageFlag.EPHEMERAL)

        if view is not None:
            # Stop listening for interactions.
            view.stop()


@plugin.include
# Register a hook to a command.
@crescent.hook(cooldowns.cooldown(1, period=period))
# Register a slash command.
@crescent.command(name="купить", description="Купить")
class Buy:
    # An option when declaring a command using class syntax.
    item = crescent.option(
        int,
        name="предмет",
        description="Предмет",
        choices=[(item.name, id__) for id__, item in shops.shop.items()],
    )

    # noinspection PyMethodMayBeStatic
    async def callback(self, context: crescent.Context) -> None:
        # Return the value for key if key is in the dictionary, else default.
        _item = str(self.item)

        item = shops.shop.get(_item)

        price = item.price

        view = View(_item)

        title = "Купить"
        description = f"Чтобы купить этот предмет потребуется `{price}` бананов"

        embed = embeds.embed("default", title=title, description=description)

        # Respond to an interaction.
        message = await context.respond(
            ensure_message=True,
            ephemeral=True,
            components=view,
            embed=embed,
        )

        if message is not None:
            try:
                # Start up the view and begin listening for interactions.
                await view.start(message)
            except Exception:
                raise


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
