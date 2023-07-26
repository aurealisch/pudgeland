import random

import crescent
import hikari

from bot.command.cooldown import cooldowns
from bot.command import _plugins
from bot.command.economy.shop import _shops
from bot.command.middleware import middlewares

plugin = _plugins.Plugin()

period = cooldowns.Period(hours=2)

name = "собирать"
deescription = "Cобирать"


class Middleware(middlewares.Middleware):
    async def callback(self, context: crescent.Context) -> None:
        # Defer this interaction response,
        # allowing you to respond within the next 15 minutes.
        await context.defer(ephemeral=False)

        contextual = str(context.user.id)

        user = await self.plugin.model.database.find_first(contextual)

        # Choose a random element from a non-empty sequence.
        collecting = random.choice(
            # Return an object that produces a sequence of integers from start
            # (inclusive) to stop (exclusive) by step.
            range(
                self.plugin.model.configuration.plugins.collect.collecting.start,
                self.plugin.model.configuration.plugins.collect.collecting.stop,
            )
        )

        if user.item:
            # Return the value for key if key is in the dictionary, else default.
            item = _shops.shop.get(str(user.item))

            # Convert a number or string to an integer,
            # or return 0 if no arguments are given.
            collecting += int(
                # Round a number to a given precision in decimal digits.
                round(collecting * item.bonus.banana)
            )

        user.banana += collecting

        # Return a capitalized version of the string.
        title = name.capitalize()
        description = f"<@{contextual}> собрал `{collecting}` бананов"

        if user.monkey:
            # Choose a random element from a non-empty sequence.
            ratio = random.choice(
                # Return an object that produces a sequence of integers from start
                # (inclusive) to stop (exclusive) by step.
                range(
                    self.plugin.model.configuration.plugins.collect.ratio.start,
                    self.plugin.model.configuration.plugins.collect.ratio.stop,
                )
            )

            monkeyish = user.monkey * (50 + ratio)

            user.banana += monkeyish

            description += f"\n+ `{monkeyish}` бананов от `{user.monkey}` обезьян"

        await self.plugin.model.database.middleware.update(
            contextual,
            banana=user.banana,
            monkey=user.monkey,
            reputation=user.reputation,
            item=user.item,
        )

        description += f"\n\n🍌 Бананы: `{user.banana}`\n🐒 Обезьяны: `{user.monkey}`"

        embed = hikari.Embed(title=title, description=description)

        # Respond to an interaction.
        await context.respond(embed=embed)


@plugin.include
# Register a hook to a command.
@crescent.hook(cooldowns.cooldown(1, period=period))
# Register a slash command.
@crescent.command(name=name, description=deescription)
class Collect:
    # noinspection PyMethodMayBeStatic
    async def callback(self, context: crescent.Context) -> None:
        return await Middleware(plugin).callback(context)


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
