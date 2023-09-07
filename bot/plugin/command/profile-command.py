from bot.common import plugins

from ._periods import period

plugin = plugins.Plugin()

commands = plugin.commands
contexts = plugin.contexts


@commands.command(
    plugin,
    name="профиль",
    description="Профиль",
    period=period,
)
async def callback(context: contexts.Context) -> None:
    _ = context.humanize

    contextual = await plugin.model.economics.find_first_or_create(str(context.user.id))

    _item = contextual.partial.item

    # fmt: off
    description = "\n".join([
        f"{context.emoji.berry} Ягоды: `{_(contextual.partial.berry)}`",
        f"{context.emoji.fox} Лисы: `{_(contextual.partial.fox)}`",
        f"📊 Репутация: `{_(contextual.partial.reputation)}`",
    ])
    # fmt: on

    if _item:
        description += f"\n✨ Предмет: `{plugin.model.economics.shop.get(_item).label}`"

    # fmt: off
    await context.respond(embed=context.embed(
        "default",
        description=description,
    ))
    # fmt: on
