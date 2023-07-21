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
import typing

import crescent
import hikari

from bot.cooldown.plugin import cooldowns
from bot.locale.plugin import locales
from bot.plugin import _plugins

plugin = _plugins.Plugin()

# 5 seconds
period = 5


@plugin.include
# Register a hook to a command.
@crescent.hook(cooldowns.cooldown(1, period=period))
# Register a slash command.
@crescent.command(
    name=locales.LocaleBuilder(
        "profile",
        ru="профиль",
        uk="профіль",
    ),
    description=locales.LocaleBuilder(
        "Profile",
        ru="Профиль",
        uk="Профіль",
    ),
)
class Profile:
    # noinspection PyMethodMayBeStatic
    async def callback(self: typing.Self, context: crescent.Context) -> None:
        locale = context.locale

        # Defer this interaction response,
        # allowing you to respond within the next 15 minutes.
        await context.defer(ephemeral=False)

        user = await plugin.model.database.find_first(str(context.user.id))

        title = locales.of(
            locale,
            locales.LocaleBuilder(
                "Profile",
                ru="Профиль",
                uk="Профіль",
            ),
        )
        description = locales.of(
            locale,
            locales.LocaleBuilder(
                f"""\
                    🍌 Bananas: `{user.banana}`
                    🐒 Monkeys: `{user.monkey}`

                    📊 Reputation: `{user.reputation}`
                """,
                ru=f"""\
                    🍌 Бананы: `{user.banana}`
                    🐒 Обезьяны: `{user.monkey}`

                    📊 Репутация: `{user.reputation}`
                """,
                uk=f"""\
                    🍌 Банан: `{user.banana}`
                    🐒 Мавпа: `{user.monkey}`

                    📊 Репутація: `{user.reputation}`
                """,
            ),
        )

        embed = hikari.Embed(title=title, description=description)

        # Respond to an interaction.
        # This function can be used multiple times for one interaction.
        await context.respond(embed=embed)
