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

from bot.cooldown.plugin import cooldowns
from bot.locale import locales
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
        "buy",
        ru="купить",
        uk="купити",
    ),
    description=locales.LocaleBuilder(
        "Buy",
        ru="Купить",
        uk="Купити",
    ),
)
class Buy:
    item = crescent.option(
        int,
        name=locales.LocaleBuilder(
            "item",
            ru="предмет",
            uk="предмет",
        ),
        description=locales.LocaleBuilder(
            "Item",
            ru="Предмет",
            uk="Предмет",
        ),
    )

    # noinspection PyMethodMayBeStatic
    async def callback(self: typing.Self, context: crescent.Context) -> None:
        await context.respond("Hello, World!")
