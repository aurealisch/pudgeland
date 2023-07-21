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

from bot.plugin import _plugins
from bot.plugin.cooldown import _cooldowns
from bot.plugin.locale import _locales

plugin = _plugins.Plugin()

# 6 hours
period = 6 * 60 * 60


@plugin.include
@crescent.hook(_cooldowns.cooldown(1, period=period))
@crescent.command(
    name=_locales.LocaleBuilder(
        "upgrade",
        ru="повысить",
        uk="пiдвищивши",
    ),
    description=_locales.LocaleBuilder(
        "Upgrade",
        ru="Повысить",
        uk="Пiдвищивши",
    ),
)
class Upgrade:
    user = crescent.option(
        hikari.User,
        name=_locales.LocaleBuilder(
            "user",
            ru="пользователь",
            uk="користувач",
        ),
        description=_locales.LocaleBuilder(
            "User",
            ru="Пользователь",
            uk="Користувач",
        ),
    )

    # noinspection PyMethodMayBeStatic
    async def callback(self: typing.Self, context: crescent.Context) -> None:
        _optional = str(self.user.id)
        _contextual = str(context.user.id)

        if _optional == _contextual:
            raise ValueError("Выбранный пользователь является автором взаимодействия")

        optional = await plugin.model.database.find_first(_optional)

        await plugin.model.database.middleware.update(
            _optional,
            banana=optional.banana,
            monkey=optional.monkey,
            reputation=optional.reputation + 1,
        )

        title = "Повысить"
        description = f"""\
            <@{_contextual}> повысил репутацию <@{_optional}>

            📈 Репутация: `{optional.reputation + 1}`
        """

        embed = hikari.Embed(title=title, description=description)

        await context.respond(embed=embed)
