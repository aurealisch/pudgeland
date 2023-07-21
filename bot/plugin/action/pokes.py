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

import collei
import crescent
import hikari

from bot.locale.plugin import locales
from bot.locale.plugin.helper import helpers
from bot.plugin import _plugins

plugin = _plugins.Plugin()


@plugin.include
# Register a slash command.
@crescent.command(
    name=locales.LocaleBuilder(
        "poke",
        ru="тыкнуть",
        uk="тицьнути",
    ),
    description=locales.LocaleBuilder(
        "Poke",
        ru="Тыкнуть пользователя",
        uk="Тицьнути користувача",
    ),
)
class Poke:
    # An option when declaring a command using class syntax.
    user = crescent.option(
        hikari.User,
        name=locales.LocaleBuilder(
            "user",
            ru="пользователь",
            uk="користувач",
        ),
        description=locales.LocaleBuilder(
            "User",
            ru="Пользователь",
            uk="Користувач",
        ),
    )

    # noinspection PyMethodMayBeStatic
    async def callback(self: typing.Self, context: crescent.Context) -> None:
        locale = context.locale

        optional = self.user.id
        contextual = context.user.id

        if optional == contextual:
            raise ValueError(
                helpers.helper(
                    locale,
                    localesBuilder=locales.LocaleBuilder(
                        "You can't do that",
                        ru="Так нельзя.",
                        uk="Так не можна",
                    ),
                )
            )

        title = helpers.helper(
            locale,
            localesBuilder=locales.LocaleBuilder(
                "Poke",
                ru="Тыкнуть",
                uk="Тицьнути",
            ),
        )
        description = helpers.helper(
            locale,
            localesBuilder=locales.LocaleBuilder(
                f"<@{context.user.id} pokes <@{self.user.id}",
                ru=f"<@{context.user.id}> тыкает <@{self.user.id}>",
                uk=f"<@{context.user.id}> тикати <@{self.user.id}>",
            ),
        )

        embed = hikari.Embed(title=title, description=description)

        # Set the image on this embed.
        embed.set_image(collei.Client().sfw.get(collei.SfwCategory.BITE).url)

        # Respond to an interaction.
        # This function can be used multiple times for one interaction.
        await context.respond(embed=embed)
