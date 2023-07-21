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

# 5 seconds
period = 5


@plugin.include
@crescent.hook(_cooldowns.cooldown(1, period=period))
@crescent.command(
    name=_locales.LocaleBuilder(
        "profile",
        ru="профиль",
        uk="профіль",
    ),
    description=_locales.LocaleBuilder(
        "Profile",
        ru="Профиль",
        uk="Профіль",
    ),
)
class Profile:
    # noinspection PyMethodMayBeStatic
    async def callback(self: typing.Self, context: crescent.Context) -> None:
        await context.defer()

        user = await plugin.model.database.find_first(str(context.user.id))

        title = "Профиль"
        description = f"""\
            🍌 Бананы: `{user.banana}`
            🐒 Обезьяны: `{user.monkey}`

            📊 Репутация: `{user.reputation}`
        """

        embed = hikari.Embed(title=title, description=description)

        await context.respond(embed=embed)
