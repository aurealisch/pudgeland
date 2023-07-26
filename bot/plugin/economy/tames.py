import random

import attrs
import crescent
import hikari
import miru

from bot.plugin._cooldown import _cooldowns
from bot.plugin import _plugins
from bot.plugin._exception import _exceptions
from bot.plugin._middleware import _middlewares

plugin = _plugins.Plugin()

period = _cooldowns.Period(seconds=5)

name = "приручать"
description = "Приручать"


# Define an *attrs* class.
@attrs.define
class View(miru.View):
    plugin: _plugins.Plugin

    # A decorator to transform a coroutine function into a Discord UI Button's callback.
    @miru.button(label="ОК", style=hikari.ButtonStyle.SECONDARY, emoji="✅")
    async def ok(self, _: miru.Button, view_context: miru.ViewContext) -> None:
        view = view_context.view

        # Short-hand method to defer an interaction response.
        await view_context.defer(ephemeral=False)

        contextual = str(view_context.user.id)

        user = await self.plugin.model.database.find_first(contextual)

        banana = user.banana
        monkey = user.monkey
        reputation = user.reputation
        item = user.item

        fed = (monkey + 1) * 250

        if fed > banana:
            raise _exceptions.NotEnoughBanana

        # Return a capitalized version of the string.
        title = name.capitalize()

        if random.choice(range(1, 10)) != 1:
            await self.plugin.model.database.middleware.update(
                contextual,
                banana=banana - fed,
                monkey=monkey,
                reputation=reputation,
                items=item,
            )

            description = f"""\
                Вы скормили 🍌 `{fed}` бананов
                и...

                ❌ Не получилось приручить обезьяну...

                ```diff\n- {fed} бананов 🍌```

                🍌 Бананы: `{banana - fed}`
                🐒 Обезьяны: `{monkey}`
            """

            embed = hikari.Embed(title=title, description=description)

            # Short-hand method to create a new message response via the interaction
            # this context represents.
            await view_context.respond(embed=embed)

            if view is not None:
                # Stop listening for interactions.
                view.stop()

            return

        await self.plugin.model.database.middleware.update(
            contextual,
            banana=banana - fed,
            monkey=monkey + 1,
            reputation=reputation,
            items=item,
        )

        description = f"""\
            Вы скормили 🍌 `{fed}` бананов
            и...

            ✅ Получилось приручить обезьяну!!!

            ```diff\n- {fed} бананов 🍌```
            ```diff\n+ 1 обезьяна 🐒```

            🍌 Бананы: `{banana - fed}`
            🐒 Обезьяны: `{monkey + 1}`
        """

        embed = hikari.Embed(title=title, description=description)

        # Short-hand method to create a new message response via the interaction
        # this context represents.
        await view_context.respond(embed=embed)

        if view is not None:
            # Stop listening for interactions.
            view.stop()

    # A decorator to transform a coroutine function into a Discord UI Button's callback.
    @miru.button(label="Отменить", style=hikari.ButtonStyle.SECONDARY, emoji="❌")
    async def cancel(self, _: miru.Button, view_context: miru.ViewContext) -> None:
        view = view_context.view

        title = "Отменить"
        description = "Отменено"

        embed = hikari.Embed(title=title, description=description)

        # Short-hand method to create a new message response via the interaction this
        # context represents.
        await view_context.respond(embed=embed, flags=hikari.MessageFlag.EPHEMERAL)

        if view is not None:
            # Stop listening for interactions.
            view.stop()


class Middleware(_middlewares.Middleware):
    async def callback(self, context: crescent.Context) -> None:
        contextual = str(context.user.id)

        user = await self.plugin.model.database.find_first(contextual)

        monkey = user.monkey

        fed = (monkey + 1) * 250

        view = View(timeout=60)

        title = "Приручать"
        description = (
            "Чтобы попробовать приручить обезьяну"
            f", потребуется скормить `{fed}` бананов"
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
            try:
                # Start up the view and begin listening for interactions.
                await view.start(message)
            except Exception:
                raise


@plugin.include
# Register a hook to a command.
@crescent.hook(_cooldowns.cooldown(1, period=period))
# Register a slash command.
@crescent.command(name=name, description="Приручать")
class Tame:
    # noinspection PyMethodMayBeStatic
    async def callback(self, context: crescent.Context) -> None:
        return await Middleware(plugin).callback(context)


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
