from bot.common import plugins

from ._groups import group
from ._periods import period

plugin = plugins.Plugin()

commands = plugin.commands
contexts = plugin.contexts


@commands.command(
    plugin,
    name="предметы",
    description="Предметы",
    period=period,
    group=group,
)
async def callback(context: contexts.Context) -> None:
    humanize = context.humanize

    shop = plugin.model.economics.shop

    # fmt: off
    description = "\n".join([
        "\n\n".join([
            f"# {item.emoji} {item.label}",
            f"> {item.description}",
            f"🏷 Цена: {context.emoji.berry} Ягоды: `{humanize(item.price)}`"
        ])
        for _, item in shop.items()
    ])
    # fmt: on

    # fmt: off
    await context.respond(embed=context.embed(
        "default",
        description=description,
    )),
    # fmt: on
