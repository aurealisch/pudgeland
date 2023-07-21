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
import random
import typing

import crescent
import hikari

from bot.plugin import _plugins
from bot.plugin.cooldown import _cooldowns
from bot.plugin.economy import _groups
from bot.plugin.locale import _locales

plugin = _plugins.Plugin()

# 5 seconds
period = 5


@_groups.group.child
@plugin.include
@crescent.hook(_cooldowns.cooldown(1, period=period))
@crescent.command(
    name=_locales.LocaleBuilder(
        "tame",
        ru="приручать",
        uk="приручати",
    ),
    description=_locales.LocaleBuilder(
        "Tame",
        ru="Приручать",
        uk="Приручати",
    ),
)
class Tame:
    # noinspection PyMethodMayBeStatic
    async def callback(self: typing.Self, context: crescent.Context) -> None:
        contextual = str(context.user.id)

        user = await plugin.model.database.find_first(contextual)

        banana = user.banana
        monkey = user.monkey
        reputation = user.reputation

        fed = (monkey + 1) * 250

        if random.choice(range(1, 10)) != 1:
            await plugin.model.database.middleware.update(
                contextual,
                banana=banana - fed,
                monkey=monkey,
                reputation=reputation,
            )

            title = "Приручать"
            description = f"""\
                Вы скормили 🍌 `{fed}` бананов
                и..

                ❌ Не получилось приручить обезьяну...

                ```diff\n- {fed} бананов 🍌```

                :banana: Бананы: `{banana - fed}`
                :monkey: Обезьяны: `{monkey}`
            """

            embed = hikari.Embed(title=title, description=description)

            await context.respond(embed=embed)

            return

        await plugin.model.database.middleware.update(
            contextual,
            banana=banana - fed,
            monkey=monkey + 1,
            reputation=reputation,
        )

        title = "Приручать"
        description = f"""\
            Вы скормили 🍌 `{fed}` бананов
            и..

            ✅ Получилось приручить обезьяну!!!

            ```diff\n- {fed} бананов 🍌```
            ```diff\n+ 1 обезьяна 🐒```

            :banana: Бананы: `{user.banana - fed}`
            :monkey: Обезьяны: `{user.monkey + 1}`
        """

        embed = hikari.Embed(title=title, description=description)

        await context.respond(embed=embed)
