import random

import crescent

from bot.common.command import commands, cooldowns, embeds
from bot.common.command.utility import utilities
from bot.common.plugin import plugins
from bot.module.economics.shop import shops

plugin = plugins.Plugin()

period = cooldowns.Period(hours=4)

_ = utilities.humanize


@plugin.include
@crescent.hook(cooldowns.cooldown(1, period=period))
@crescent.command(name="собирать", description="Cобирать")
class Command(commands.Command):
    async def run(self, context: crescent.Context) -> None:
        await context.defer()

        _contextual = str(context.user.id)

        contextual = await plugin.model.database.find_first(_contextual)

        monkey = contextual.monkey

        _item = contextual.item

        collect = plugin.model.configuration.plugins.collect

        total = 0

        collecting = random.randint(
            collect.collecting.a,
            b=collect.collecting.b,
        )

        if _item:
            item = shops.shop.get(str(_item))

            bonus = item.bonus

            if bonus.banana:
                collecting += int(round(collecting * bonus.banana))

        total += collecting

        description = f"<@{_contextual}> собрал 🍌 `{_(collecting)}` бананов"

        if monkey:
            monkeying = monkey * random.randint(
                collect.monkeying.a,
                b=collect.monkeying.b,
            )

            if _item:
                item = shops.shop.get(str(_item))

                bonus = item.bonus

                if bonus.monkey:
                    monkeying += int(round(monkeying * bonus.monkey))

            total += monkeying

            # fmt: off
            description += (
                f"\n+ 🍌 `{_(monkeying)}` бананов от 🐒 `{_(monkey)}` обезьян"
            )
            # fmt: on

            description += f"\n\n✨ Всего: 🍌 `{_(total)}` бананов"

        await plugin.model.database.update(
            _contextual,
            banana=contextual.banana + total,
            monkey=monkey,
            reputation=contextual.reputation,
            item=contextual.item,
        )

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
