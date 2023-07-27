import random

import crescent

from bot.command.cooldown import cooldowns
from bot.command.plugin import _plugins
from bot.shop import shops
from bot.utility import embeds

plugin = _plugins.Plugin()

period = cooldowns.Period(hours=2)

name = "собирать"
deescription = "Cобирать"


@plugin.include
# Register a hook to a command.
@crescent.hook(cooldowns.cooldown(1, period=period))
# Register a slash command.
@crescent.command(name=name, description=deescription)
class Collect:
    # noinspection PyMethodMayBeStatic
    async def callback(self, context: crescent.Context) -> None:
        # Defer this interaction response,
        # allowing you to respond within the next 15 minutes.
        await context.defer()

        _contextish = str(context.user.id)

        contextish = await self.plugin.model.database.find_first(_contextish)

        banana = contextish.banana
        monkey = contextish.monkey
        reputation = contextish.reputation
        item = contextish.item

        total = 0

        # Choose a random element from a non-empty sequence.
        collecting = random.choice(
            # Return an object that produces a sequence of integers from start
            # (inclusive) to stop (exclusive) by step.
            range(
                self.plugin.model.configuration.plugins.collect.collecting.start,
                self.plugin.model.configuration.plugins.collect.collecting.stop,
            )
        )

        if item:
            # Return the value for key if key is in the dictionary, else default.
            _item = shops.shop.get(str(item))

            # Convert a number or string to an integer,
            # or return 0 if no arguments are given.
            collecting += int(
                # Round a number to a given precision in decimal digits.
                round(collecting * _item.bonus.banana)
            )

        total += collecting

        # Return a capitalized version of the string.
        title = name.capitalize()
        description = f"<@{_contextish}> собрал `{collecting}` бананов"

        if monkey:
            # Choose a random element from a non-empty sequence.
            ratio = random.choice(
                # Return an object that produces a sequence of integers from start
                # (inclusive) to stop (exclusive) by step.
                range(
                    self.plugin.model.configuration.plugins.collect.ratio.start,
                    self.plugin.model.configuration.plugins.collect.ratio.stop,
                )
            )

            monkeyish = monkey * (50 + ratio)

            total += monkeyish

            description += f"\n+ `{monkeyish}` бананов от `{monkey}` обезьян"

        banana += total

        await self.plugin.model.database.middleware.update(
            contextish,
            banana=banana,
            monkey=monkey,
            reputation=reputation,
            item=item,
        )

        description += f"\n\n```diff\n+ {total} бананов 🍌```"

        embed = embeds.embed("default", title=title, description=description)

        # Respond to an interaction.
        await context.respond(embed=embed)


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
