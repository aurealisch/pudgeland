import random
import typing

import crescent

from bot.common import contexts, plugins, shops
from bot.common.abc import commands
from bot.common.command import cooldowns

from . import _groups, _periods

plugin = plugins.Plugin()


@typing.final
@_groups.group.child
@plugin.include
@crescent.hook(cooldowns.cooldown(period=_periods.period))
@crescent.command(name="собрать", description="Собрать ягоды")
class CollectCommand(commands.CommandABC):
    async def run(self, context: contexts.Context) -> None:
        await context.defer()

        _contextual = str(context.user.id)

        contextual = await plugin.model.economics.find_first_or_create(_contextual)

        fox = contextual.partial.fox

        _item = contextual.partial.item

        collect = plugin.model.configuration.plugins.collect
        events = plugin.model.economics.events

        total = 0

        berrying = random.choice(range(collect.berrying.a, b=collect.berrying.b))

        if events:
            for event in events:
                buff = event.buff

                if buff:
                    _berry = buff.berry

                    berrying *= _berry

        if _item:
            item = shops.shop.get(_item)

            bonus = item.bonus

            if bonus.berry:
                berrying += round(berrying * bonus.berry)

        berrying = round(berrying)

        total += berrying

        description = f"<@{_contextual}> собрал {context.emoji.berry} `{context.humanize(berrying)}` ягод"  # noqa: E501

        if fox:
            foxying = fox * random.choice(range(collect.foxying.a, b=collect.foxying.b))

            if events:
                for event in events:
                    buff = event.buff

                    if buff:
                        _fox = buff.fox

                        foxying *= _fox

            if _item:
                item = shops.shop.get(_item)

                bonus = item.bonus

                if bonus.fox:
                    foxying += round(foxying * bonus.fox)

            foxying = round(foxying)

            total += foxying

            description += f"\n+ {context.emoji.berry} `{context.humanize(foxying)}` ягод от {context.emoji.fox} `{context.humanize(fox)}` лис"  # noqa: E501

            description += f"\n\n🔁 Всего: {context.emoji.berry} `{context.humanize(total)}` ягод"  # noqa: E501'

        await contextual.berry.add(total)

        await context.respond(embed=context.embed("default", description=description))
