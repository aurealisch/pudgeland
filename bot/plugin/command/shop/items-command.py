import string
import typing

import crescent

from bot.common import contexts, plugins, shops
from bot.common.abc import commands
from bot.common.command import cooldowns

from . import _groups

plugin = plugins.Plugin()

period = cooldowns.Period(seconds=2, milliseconds=500)  # 2.5 seconds


@typing.final
@_groups.group.child
@plugin.include
@crescent.hook(cooldowns.cooldown(period=period))
@crescent.command(name="предметы", description="Предметы")
class PreviewCommand(commands.CommandABC):
    async def run(self, context: contexts.Context) -> None:
        await context.defer(True)

        description = string.whitespace

        for value, item in shops.shop.items():
            description += f"""
                # {value}. {item.emoji} **{item.label}**

                > {item.description}

                🏷 Цена: {context.emoji.berry} Ягоды: `{context.humanize(item.price)}`
            """

        await context.respond(
            ephemeral=True,
            embed=context.embed(
                "default",
                description=description,
            ),
        )
