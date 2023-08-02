import random

import crescent

from bot.common.command import commands
from bot.common.command.cooldown import cooldowns
from bot.common.command.embed import embeds
from bot.common.plugin import plugins
from bot.module.economics.shop import shops

plugin = plugins.Plugin()

period = cooldowns.Period(hours=2)


@plugin.include
@crescent.hook(cooldowns.cooldown(1, period=period))
@crescent.command(name="собирать", description="Cобирать")
class Command(commands.Command):
    async def run(self, context: crescent.Context) -> None:
        _contextual = str(context.user.id)

        contextual = await plugin.model.database.find_first(_contextual)

        monkey = contextual.monkey

        _item = contextual.item

        if _item:
            item = shops.shop.get(str(_item))

            bonus = item.bonus

        collect = plugin.model.configuration.plugins.collect

        total = 0

        collecting = random.randint(
            collect.collecting.a,
            b=collect.collecting.b,
        )

        try:
            if bonus.monkey:
                collecting += collecting * bonus.monkey
        except TypeError:
            pass

        total += collecting

        description = f"{_contextual} собрал 🍌 `{collecting}` бананов"

        if monkey:
            monkeying = monkey * random.randint(
                collect.monkeying.a,
                b=collect.monkeying.b,
            )

            try:
                if bonus.monkey:
                    monkeying += monkeying * bonus.monkey
            except TypeError:
                pass

            total += monkeying

            description += f"\n+ 🍌 `{monkeying}` бананов от 🐒 `{monkey}` обезьян"

        description += f"\n\n✨ Всего: 🍌 `{total}` бананов"

        await plugin.model.database.middleware.update(
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
