import string

from bot.common import plugins

from ._groups import group
from ._periods import period

plugin = plugins.Plugin()


@plugin.include
@plugin.commands.command(
    "предметы",
    description="Предметы",
    period=period,
    group=group,
)
async def callback(context: plugin.contexts.Context) -> None:
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
