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
from __future__ import annotations

__all__: typing.Sequence[str] = ("plugin", "Kill")

import typing

import crescent
import hikari

from bot.plugin import _action, plugins
from bot.plugin.locale import locales
from bot.plugin.middleware._action import kills

plugin = plugins.Plugin()


@_action.group.child
@plugin.include
@crescent.command(
    name=locales.LocaleBuilder(
        "kill",
        russian="убить",
        ukrainian="вбивати",
    ),
    description=locales.LocaleBuilder(
        "Kill",
        russian="Убить пользователя",
        ukrainian="Вбивати користувача",
    ),
)
class Kill:
    user = crescent.option(
        hikari.User,
        name=locales.LocaleBuilder(
            "user",
            russian="пользователь",
            ukrainian="користувач",
        ),
        description=locales.LocaleBuilder(
            "User",
            russian="Пользователь",
            ukrainian="Користувач",
        ),
    )

    # noinspection PyMethodMayBeStatic
    async def callback(self, context: crescent.Context) -> None:
        """
        Parameters
        ----------
        - `context` : `crescent.Context`
        """
        await kills.Middleware(plugin).callback(context)
