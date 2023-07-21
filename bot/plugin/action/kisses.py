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
import string
import typing

import collei
import crescent
import hikari

from bot.locale.plugin import locales
from bot.locale.plugin.helper import helpers
from bot.plugin import _plugins

plugin = _plugins.Plugin()


@plugin.include
@crescent.command(
    name=locales.LocaleBuilder(
        "kiss",
        ru="поцеловать",
        uk="поцілувати",
    ),
    description=locales.LocaleBuilder(
        "Kiss the user",
        ru="Поцеловать пользователя",
        uk="Поцілувати користувача",
    ),
)
class Kiss:
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
                        ru="Так нельзя",
                        uk="Так не можна",
                    ),
                )
            )

        title = helpers.helper(
            locale,
            localesBuilder=locales.LocaleBuilder(
                "Kiss",
                ru="Поцеловать",
                uk="Поцілувати",
            ),
        )

        template = string.Template(f"<@{contextual}> $action <@{optional}>")

        description = helpers.helper(
            locale,
            localesBuilder=locales.LocaleBuilder(
                template.substitute({"action": "kisses"}),
                ru=template.substitute({"action": "целует"}),
                uk=template.substitute({"action": "цілувати"}),
            ),
        )

        embed = hikari.Embed(title=title, description=description)

        # Set the image on this embed.
        embed.set_image(collei.Client().sfw.get(collei.SfwCategory.KISS).url)

        # Respond to an interaction.
        # This function can be used multiple times for one interaction.
        await context.respond(embed=embed)
