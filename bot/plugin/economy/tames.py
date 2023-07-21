# -*- coding: utf-8 -*-
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
import random
import typing

import crescent
import hikari
import miru

from bot.cooldown.plugin import cooldowns
from bot.locale.plugin import locales
from bot.plugin import _plugins

plugin = _plugins.Plugin()

# 5 seconds
period = 5


class View(miru.View):
    # A decorator to transform a coroutine function into a Discord UI Button's callback.
    # This must be inside a subclass of View.
    @miru.button(label="ОК", style=hikari.ButtonStyle.SECONDARY, emoji="✅")
    async def ok(self, _: miru.Button, view_context: miru.ViewContext) -> None:
        view = view_context.view

        # Short-hand method to defer an interaction response.
        # Raises RuntimeError if the interaction was already responded to.
        await view_context.defer(ephemeral=False)

        contextual = str(view_context.user.id)

        user = await plugin.model.database.find_first(contextual)

        banana = user.banana
        monkey = user.monkey
        reputation = user.reputation

        fed = (monkey + 1) * 250

        if fed > banana:
            raise ValueError("Недостаточно бананов")

        if random.choice(range(1, 10)) != 1:
            await plugin.model.database.middleware.update(
                contextual,
                banana=banana - fed,
                monkey=monkey,
                reputation=reputation,
            )

            title = "Приручать"
            description = f"""\
                Вы скормили 🍌 `{fed}` бананов
                и..

                ❌ Не получилось приручить обезьяну...

                ```diff- {fed} бананов 🍌```

                :banana: Бананы: `{banana - fed}`
                :monkey: Обезьяны: `{monkey}`
            """

            embed = hikari.Embed(title=title, description=description)

            # Short-hand method to create a new message response via the interaction
            # this context represents.
            await view_context.respond(embed=embed)

            if view is not None:
                # Stop listening for interactions.
                view.stop()

            return

        await plugin.model.database.middleware.update(
            contextual,
            banana=banana - fed,
            monkey=monkey + 1,
            reputation=reputation,
        )

        title = "Приручать"
        description = f"""\
            Вы скормили 🍌 `{fed}` бананов
            и..

            ✅ Получилось приручить обезьяну!!!

            ```diff\n- {fed} бананов 🍌```
            ```diff\n+ 1 обезьяна 🐒```

            :banana: Бананы: `{user.banana - fed}`
            :monkey: Обезьяны: `{user.monkey + 1}`
        """

        embed = hikari.Embed(title=title, description=description)

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
        "tame",
        ru="приручать",
        uk="приручати",
    ),
    description=locales.LocaleBuilder(
        "Tame",
        ru="Приручать",
        uk="Приручати",
    ),
)
class Tame:
    # noinspection PyMethodMayBeStatic
    async def callback(self: typing.Self, context: crescent.Context) -> None:
        contextual = str(context.user.id)

        user = await plugin.model.database.find_first(contextual)

        monkey = user.monkey

        fed = (monkey + 1) * 250

        title = "Приручать"
        description = f"""\
            Чтобы попробовать приручить обезьяну потребуется скормить `{fed}` бананов
        """

        embed = hikari.Embed(title=title, description=description)

        view = View(timeout=60)

        # Respond to an interaction.
        # This function can be used multiple times for one interaction.
        message = await context.respond(
            ensure_message=True, ephemeral=True, components=view, embed=embed
        )

        if message is not None:
            # Start up the view and begin listening for interactions.
            await view.start(message)
