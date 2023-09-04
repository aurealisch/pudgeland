import string

from bot.common import plugins
from bot.common.command import commands, contexts, cooldowns

from . import _groups

plugin = plugins.Plugin()


@plugin.include
@commands.command(
    "предметы",
    description="Предметы",
    period=cooldowns.Period(
        seconds=2,
        milliseconds=500,
    ),  # 2.5 seconds
    group=_groups.group,
)
async def callback(context: contexts.Context) -> None:
    await context.defer(True)

    description = string.whitespace

    for value, item in plugin.model.economics.shop.items():
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
