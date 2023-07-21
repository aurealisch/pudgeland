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
from bot.cooldown.plugin import cooldowns
from bot.locale.plugin import locales

plugin = _plugins.Plugin()


# 2 hours
period = 2 * 60 * 60


@plugin.include
# Register a hook to a command.
@crescent.hook(cooldowns.cooldown(1, period=period))
# Register a slash command.
@crescent.command(
    name=locales.LocaleBuilder(
        "collect",
        ru="собирать",
        uk="збирати",
    ),
    description=locales.LocaleBuilder(
        "Сollect",
        ru="Cобирать",
        uk="Збирати",
    ),
)
class Collect:
    # noinspection PyMethodMayBeStatic
    async def callback(self: typing.Self, context: crescent.Context) -> None:
        # Defer this interaction response,
        # allowing you to respond within the next 15 minutes.
        await context.defer(ephemeral=False)

        contextual = str(context.user.id)

        user = await plugin.model.database.find_first(contextual)

        banana = user.banana
        monkey = user.monkey
        reputation = user.reputation

        # Choose a random element from a non-empty sequence.
        collecting = random.choice(
            range(
                plugin.model.configuration.plugins.collect.minimal,
                plugin.model.configuration.plugins.collect.maximum,
            )
        )

        banana += collecting

        title = "Собирать"
        description = f"""\
            <@{contextual}> собрал `{collecting}` бананов
        """

        if monkey != 0:
            # Choose a random element from a non-empty sequence.
            ratio = random.choice(range(1, 50))

            monkeyish = monkey * (50 + ratio)

            banana += monkeyish

            description += f"\n+ `{monkeyish}` бананов от `{monkey}` обезьян"

        await plugin.model.database.middleware.update(
            contextual,
            banana=banana,
            monkey=monkey,
            reputation=reputation,
        )

        description += f"""\
            \n\n
            :banana: Бананы: `{banana}`
            :monkey: Обезьяны: `{monkey}`
        """

        embed = hikari.Embed(title=title, description=description)

        # Respond to an interaction.
        # This function can be used multiple times for one interaction
        await context.respond(embed=embed)
