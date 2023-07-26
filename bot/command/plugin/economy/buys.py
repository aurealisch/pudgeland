import attrs
import crescent
import hikari
import miru

from bot.command import _plugins
from bot.command.cooldown import cooldowns
from bot.command.error import errors
from bot.command.middleware import middlewares
from bot.command.plugin.economy.shop import _items, _shops
from bot.utility import embeds

plugin = _plugins.Plugin()

period = cooldowns.Period(seconds=5)

name = "купить"
description = "Купить"


@attrs.define
class View(miru.View):
    plugin: _plugins.Plugin

    item: _items.Id

    # A decorator to transform a coroutine function into a Discord UI Button's callback.
    @miru.button(label="ОК", style=hikari.ButtonStyle.SECONDARY, emoji="✅")
    async def ok(self, _: miru.Button, view_context: miru.ViewContext) -> None:
        view = view_context.view

        # Short-hand method to defer an interaction response.
        await view_context.defer(ephemeral=False)

        id__ = str(view_context.user.id)

        user = await self.plugin.model.database.find_first(id__)

        # Return the value for key if key is in the dictionary, else default.
        item = _shops.shop.get(self.item)

        if item.price > user.banana:
            raise errors.NotEnoughBanana

        if int(self.item) == user.item:
            raise ValueError

        await self.plugin.model.database.middleware.update(
            id__,
            banana=user.banana - item.price,
            monkey=user.monkey,
            reputation=user.reputation,
            item=int(self.item),
        )

        # Return a capitalized version of the string.
        title = name.capitalize()
        description = f"""\
            <@{user.id}> купил `{item.name}` за `{item.price}` бананов

            ```diff\n- {item.price} бананов 🍌```
            ```diff\n+ {item.name}```
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


class Middleware(middlewares.Middleware):
    async def callback(self, context: crescent.Context) -> None:
        # Return the value for key if key is in the dictionary, else default.
        item = _shops.shop.get(str(self.item))

        price = item.price

        view = View(str(self.item), timeout=60)

        # Return a capitalized version of the string.
        title = name.capitalize()
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


@plugin.include
# Register a hook to a command.
@crescent.hook(cooldowns.cooldown(1, period=period))
# Register a slash command.
@crescent.command(name=name, description=description)
class Buy:
    # An option when declaring a command using class syntax.
    item = crescent.option(
        int,
        name="предмет",
        description="Предмет",
        choices=[(item.name, id__) for id__, item in _shops.shop.items()],
    )

    # noinspection PyMethodMayBeStatic
    async def callback(self, context: crescent.Context) -> None:
        return await Middleware(plugin, {"item": self.item}).callback(context)


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
