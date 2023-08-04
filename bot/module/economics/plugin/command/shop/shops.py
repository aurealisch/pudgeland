import string

import crescent

from bot.common.command import commands, cooldowns, embeds
from bot.common.command.utility import utilities
from bot.common.plugin import plugins
from bot.module.economics.shop import shops

plugin = plugins.Plugin()

period = cooldowns.Period(seconds=2.5)

_ = utilities.humanize


@plugin.include
@crescent.hook(cooldowns.cooldown(1, period=period))
@crescent.command(name="магазин", description="Магазин")
class Command(commands.Command):
    async def run(self, context: crescent.Context) -> None:
        description = string.whitespace

        for value, item in shops.shop.items():
            label = item.label
            _description = item.description

            emoji = item.emoji

            price = item.price

            description += f"# {value}. {emoji} **{label}**\n> {_description}\n\n🏷 Цена: 🍌 Бананы: `{_(price)}`\n"  # noqa: E501

        embed = embeds.embed(
            "default",
            context=context,
            description=description,
        )

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
