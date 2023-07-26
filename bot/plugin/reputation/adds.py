import string

import crescent
import hikari

from bot.cooldown.plugin import cooldowns
from bot.locale import locales
from bot.plugin import _plugins
from bot.plugin.reputation import _groups

plugin = _plugins.Plugin()

# 6 hours
period = 6 * 60 * 60


# Add a command to this command group.
@_groups.group.child
@plugin.include
# Register a hook to a command.
@crescent.hook(cooldowns.cooldown(1, period=period))
# Register a slash command.
@crescent.command(
    name=locales.LocaleBuilder(
        "add",
        ru="добавить",
        uk="додавши",
    ),
    description=locales.LocaleBuilder(
        "Add",
        ru="Добавить",
        uk="Додавши",
    ),
)
class Add:
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

        # Defer this interaction response,
        # allowing you to respond within the next 15 minutes.
        await context.defer(ephemeral=False)

        _optional = str(self.user.id)
        _contextual = str(context.user.id)

        if _optional == _contextual:
            raise ValueError(
                locales.of(
                    locale,
                    locale_builder=locales.LocaleBuilder(
                        "You can't do that",
                        ru="Так нельзя",
                        uk="Так не можна",
                    ),
                )
            )

        optional = await plugin.model.database.find_first(_optional)

        await plugin.model.database.middleware.update(
            _optional,
            banana=optional.banana,
            monkey=optional.monkey,
            reputation=optional.reputation + 1,
            item=optional.item,
        )

        title = locales.of(
            locale,
            locale_builder=locales.LocaleBuilder(
                "Add",
                ru="Добавить",
                uk="Додавши",
            ),
        )

        template = string.Template(
            f"""
                <@{_contextual}> $action <@{_optional}>

                📈 $reputation: `{optional.reputation + 1}`
            """
        )

        description = locales.of(
            locale,
            locale_builder=locales.LocaleBuilder(
                f"""
                    <@{_contextual}> added a reputation <@{_optional}>

                    📈 Reputation: `{optional.reputation + 1}`
                """,
                ru=template.substitute(
                    dict(
                        action="добавил репутацию",
                        reputation="Репутация",
                    ),
                ),
                uk=template.substitute(
                    dict(
                        action="додав репутацію",
                        reputation="Репутація",
                    ),
                ),
            ),
        )

        embed = hikari.Embed(title=title, description=description)

        # Respond to an interaction.
        await context.respond(embed=embed)


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
