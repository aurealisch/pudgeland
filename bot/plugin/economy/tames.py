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
import miru

from bot.cooldown.plugin import cooldowns
from bot.locale.plugin import locales
from bot.plugin import _plugins

plugin = _plugins.Plugin()

# 5 seconds
period = 5


class View(miru.View):
    # A decorator to transform a coroutine function into a Discord UI Button's callback.
    # This must be inside a subclass of View.
    @miru.button(label="ОК", style=hikari.ButtonStyle.SECONDARY, emoji="✅")
    async def ok(self, _: miru.Button, view_context: miru.ViewContext) -> None:
        locale = view_context.locale

        view = view_context.view

        # Short-hand method to defer an interaction response.
        # Raises RuntimeError if the interaction was already responded to.
        await view_context.defer(ephemeral=False)

        contextual = str(view_context.user.id)

        user = await plugin.model.database.find_first(contextual)

        banana = user.banana
        monkey = user.monkey
        reputation = user.reputation

        fed = (monkey + 1) * 250

        if fed > banana:
            raise ValueError(
                locales.of(
                    locale,
                    locale_builder=locales.LocaleBuilder(
                        "Not enough bananas",
                        ru="Недостаточно бананов",
                        uk="Недостатньо бананів",
                    ),
                )
            )

        title = locales.of(
            locale,
            locale_builder=locales.LocaleBuilder(
                "Tame",
                ru="Приручать",
                uk="Приручати",
            ),
        )

        if random.choice(range(1, 10)) != 1:
            await plugin.model.database.middleware.update(
                contextual,
                banana=banana - fed,
                monkey=monkey,
                reputation=reputation,
            )

            template = string.Template(
                f"""\
                    $you $fed 🍌 `{fed}` $bananas1
                    $and...

                    ❌ $failedToTameTheMonkey...

                    ```diff\n- {fed} $bananas1 🍌```

                    🍌 $bananas2: `{banana - fed}`
                    🐒 $monkeys: `{monkey}`
                """
            )

            description = locales.of(
                locale,
                locale_builder=locales.LocaleBuilder(
                    f"""\
                        You fed 🍌 `{fed}` bananas
                        and...

                        ❌ Failed to tame the monkey...

                        ```diff\n- {fed} bananas 🍌```

                        🍌 Bananas: `{banana - fed}`
                        🐒 Monkeys: `{monkey}`
                    """,
                    ru=template.substitute(
                        {
                            "you": "Вы",
                            "fed": "скормили",
                            "bananas1": "бананов",
                            "and": "и",
                            "failedToTameTheMonkey": "Не получилось приручить обезьяну",
                            "bananas2": "Бананы",
                            "monkeys": "Обезьян",
                        },
                    ),
                    uk=template.substitute(
                        {
                            "you": "Ви",
                            "fed": "нагодували",
                            "bananas1": "бананів",
                            "and": "і",
                            "failedToTameTheMonkey": "Не вийшло приручити мавпу",
                            "bananas2": "Банан",
                            "monkeys": "Мавпа",
                        },
                    ),
                ),
            )

            embed = hikari.Embed(title=title, description=description)

            # Short-hand method to create a new message response via the interaction
            # this context represents.
            await view_context.respond(embed=embed)

            if view is not None:
                # Stop listening for interactions.
                view.stop()

            return

        await plugin.model.database.middleware.update(
            contextual,
            banana=banana - fed,
            monkey=monkey + 1,
            reputation=reputation,
        )

        template = string.Template(
            f"""\
                $you $fed 🍌 `{fed}` $bananas1
                $and...

                ✅ $itTurnedOutToTameAMonkey!!!

                ```diff\n- {fed} $bananas1 🍌```
                ```diff\n+ 1 $monkey 🐒```

                🍌 $bananas2: `{banana - fed}`
                🐒 $monkeys: `{monkey + 1}`
            """
        )

        description = locales.of(
            locale,
            locale_builder=locales.LocaleBuilder(
                f"""\
                    You fed 🍌 `{fed}` bananas
                    and...

                    ✅ It turned out to tame a monkey!!!

                    ```diff\n- {fed} bananas 🍌```
                    ```diff\n+ 1 monkey 🐒```

                    🍌 Bananas: `{banana - fed}`
                    🐒 Monkeys: `{monkey + 1}`
                """,
                ru=template.substitute(
                    {
                        "you": "Вы",
                        "fed": "скормили",
                        "bananas1": "бананов",
                        "and": "и",
                        "itTurnedOutToTameAMonkey": "Получилось приручить обезьяну",
                        "bananas2": "Бананы",
                        "monkeys": "Обезьян",
                    },
                ),
                uk=template.substitute(
                    {
                        "you": "Ви",
                        "fed": "нагодували",
                        "bananas1": "бананів",
                        "and": "і",
                        "itTurnedOutToTameAMonkey": "Вийшло приручити мавпу",
                        "bananas2": "Банан",
                        "monkeys": "Мавпа",
                    },
                ),
            ),
        )

        embed = hikari.Embed(title=title, description=description)

        # Short-hand method to create a new message response via the interaction
        # this context represents.
        await view_context.respond(embed=embed)

        if view is not None:
            # Stop listening for interactions.
            view.stop()

    # A decorator to transform a coroutine function into a Discord UI Button's callback.
    # This must be inside a subclass of View.
    @miru.button(label="Отменить", style=hikari.ButtonStyle.SECONDARY, emoji="❌")
    async def cancel(self, _: miru.Button, view_context: miru.ViewContext) -> None:
        locale = view_context.locale

        view = view_context.view

        title = locales.of(
            locale,
            locale_builder=locales.LocaleBuilder(
                "Cancel",
                ru="Отменить",
                uk="Відмінивши",
            ),
        )
        description = locales.of(
            locale,
            locale_builder=locales.LocaleBuilder(
                "Cancelled",
                ru="Отменено",
                uk="Скасований",
            ),
        )

        embed = hikari.Embed(title=title, description=description)

        # Short-hand method to create a new message response via the interaction this
        # context represents.
        await view_context.respond(embed=embed, flags=hikari.MessageFlag.EPHEMERAL)

        if view is not None:
            # Stop listening for interactions.
            view.stop()


@plugin.include
# Register a hook to a command.
@crescent.hook(cooldowns.cooldown(1, period=period))
# Register a slash command.
@crescent.command(
    name=locales.LocaleBuilder(
        "tame",
        ru="приручать",
        uk="приручати",
    ),
    description=locales.LocaleBuilder(
        "Tame",
        ru="Приручать",
        uk="Приручати",
    ),
)
class Tame:
    # noinspection PyMethodMayBeStatic
    async def callback(self: typing.Self, context: crescent.Context) -> None:
        locale = context.locale

        contextual = str(context.user.id)

        user = await plugin.model.database.find_first(contextual)

        monkey = user.monkey

        fed = (monkey + 1) * 250

        title = locales.of(
            locale,
            locale_builder=locales.LocaleBuilder(
                "Tame",
                ru="Приручать",
                uk="Приручати",
            ),
        )

        template = string.Template(
            f"$toTryToTameAMonkey, $youWillNeedToFeed `{fed}` $bananas"
        )

        description = locales.of(
            locale,
            locale_builder=locales.LocaleBuilder(
                f"To try to tame a monkey, you will need to feed `{fed}` bananas",
                ru=template.substitute(
                    {
                        "toTryToTameAMonkey": "Чтобы попробовать приручить обезьяну",
                        "youWillNeedToFeed": "потребуется скормить",
                        "bananas": "бананов",
                    }
                ),
                uk=template.substitute(
                    {
                        "toTryToTameAMonkey": "Щоб спробувати приручити мавпу",
                        "youWillNeedToFeed": "потрібно згодувати ",
                        "bananas": "бананів",
                    }
                ),
            ),
        )

        embed = hikari.Embed(title=title, description=description)

        view = View(timeout=60)

        # Respond to an interaction.
        # This function can be used multiple times for one interaction.
        message = await context.respond(
            ensure_message=True, ephemeral=True, components=view, embed=embed
        )

        if message is not None:
            # Start up the view and begin listening for interactions.
            await view.start(message)
