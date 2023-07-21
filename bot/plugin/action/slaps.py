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

from bot.plugin import _plugins
from bot.plugin.locale import _locales
from bot.plugin.action import _groups

plugin = _plugins.Plugin()


@_groups.group.child
@plugin.include
@crescent.command(
    name=_locales.LocaleBuilder(
        "slap",
        ru="шлёпнуть",
        uk="шльопнути",
    ),
    description=_locales.LocaleBuilder(
        "Slap",
        ru="Шлёпнуть пользователя",
        uk="Шльопнути користувача",
    ),
)
class Slap:
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
        optional = self.user.id
        contextual = context.user.id

        if optional == contextual:
            raise ValueError("Выбранный пользователь является автором взаимодействия")

        title = "Шлёпнуть"
        description = f"<@{context.user.id}> шлёпнул(а) <@{self.user.id}>"

        embed = hikari.Embed(title=title, description=description)

        embed.set_image(collei.Client().sfw.get(collei.SfwCategory.BITE).url)

        await context.respond(embed=embed)
