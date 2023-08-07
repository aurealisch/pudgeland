import string

import crescent

from bot.common.command import commands, cooldowns, embeds, utilities
from bot.common.plugin import plugins
from bot.common.shop import shops

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
