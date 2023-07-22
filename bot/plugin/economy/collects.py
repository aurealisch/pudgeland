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
import string
import typing

import crescent
import hikari

from bot.cooldown.plugin import cooldowns
from bot.locale import locales
from bot.plugin import _plugins

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
        locale = context.locale

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
            # Return an object that produces a sequence of integers from start
            # (inclusive) to stop (exclusive) by step
            range(
                plugin.model.configuration.plugins.collect.collecting.start,
                plugin.model.configuration.plugins.collect.collecting.stop,
            )
        )

        banana += collecting

        title = locales.of(
            locale,
            locale_builder=locales.LocaleBuilder(
                "Collect",
                ru="Собирать",
                uk="Збирати",
            ),
        )

        template = string.Template(
            f"<@{contextual}> $collected `{collecting}` $bananas"
        )

        description = locales.of(
            locale,
            locale_builder=locales.LocaleBuilder(
                f"<@{contextual} collected `{collecting}` bananas",
                ru=template.substitute(dict(collected="собрал", bananas="бананов")),
                uk=template.substitute(dict(collected="зібрав", bananas="бананів")),
            ),
        )

        if monkey != 0:
            # Choose a random element from a non-empty sequence.
            ratio = random.choice(
                # Return an object that produces a sequence of integers from start
                # (inclusive) to stop (exclusive) by step
                range(
                    plugin.model.configuration.plugins.collect.ratio.start,
                    plugin.model.configuration.plugins.collect.ratio.stop,
                )
            )

            monkeyish = monkey * (50 + ratio)

            banana += monkeyish

            template = string.Template(
                f"\n+ `{monkeyish}` $bananas $from__ `{monkey}` $monkeys"
            )

            description += locales.of(
                locale,
                locale_builder=locales.LocaleBuilder(
                    f"\n+ `{monkeyish}` bananas from `{monkey}` monkeys",
                    ru=template.substitute(
                        dict(
                            bananas="бананов",
                            from__="от",
                            monkeys="обезьян",
                        ),
                    ),
                    uk=template.substitute(
                        dict(
                            bananas="бананів",
                            from__="від",
                            monkeys="мавп",
                        ),
                    ),
                ),
            )

        await plugin.model.database.middleware.update(
            contextual,
            banana=banana,
            monkey=monkey,
            reputation=reputation,
        )

        template = string.Template(
            f"\n\n🍌 $bananas: `{banana}`\n🐒 $monkeys: `{monkey}`"
        )

        description += locales.of(
            locale,
            locale_builder=locales.LocaleBuilder(
                f"\n\n🍌 Bananas: `{banana}`\n🐒 Monkeys: `{monkey}`",
                ru=template.substitute(dict(bananas="Бананы", monkeys="Обезьяны")),
                uk=template.substitute(dict(bananas="Банан", monkeys="Мавпа")),
            ),
        )

        embed = hikari.Embed(title=title, description=description)

        # Respond to an interaction.
        await context.respond(embed=embed)
