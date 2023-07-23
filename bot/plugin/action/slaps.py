import string

import collei
import crescent
import hikari

from bot.exception import exceptions
from bot.locale import locales
from bot.plugin import _plugins

plugin = _plugins.Plugin()


@plugin.include
# Register a slash command.
@crescent.command(
    name=locales.LocaleBuilder(
        "slap",
        ru="шлёпнуть",
        uk="шльопнути",
    ),
    description=locales.LocaleBuilder(
        "Slap",
        ru="Шлёпнуть пользователя",
        uk="Шльопнути користувача",
    ),
)
class Slap:
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
    async def callback(self, context: crescent.Context) -> None:
        locale = context.locale

        optional = self.user.id
        contextual = context.user.id

        if optional == contextual:
            raise exceptions.YouCantDoThat(locale)

        title = locales.of(
            locale,
            locale_builder=locales.LocaleBuilder(
                "Slap",
                ru="Шлёпнуть",
                uk="Шльопнути",
            ),
        )

        template = string.Template(f"<@{contextual}> $action <@{optional}>")

        description = locales.of(
            locale,
            locale_builder=locales.LocaleBuilder(
                template.substitute(dict(action="slaps")),
                ru=template.substitute(dict(action="шлёпает")),
                uk=template.substitute(dict(action="шльопати")),
            ),
        )

        embed = hikari.Embed(title=title, description=description)

        # Set the image on this embed.
        embed.set_image(collei.Client().sfw.get(collei.SfwCategory.BITE).url)

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
