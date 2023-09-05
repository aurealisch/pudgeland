from bot.common import plugins

from ._periods import period

plugin = plugins.Plugin()


@plugin.commands.command(
    plugin,
    name="профиль",
    description="Профиль",
    period=period,
)
async def callback(context: plugin.contexts.Context) -> None:
    await context.defer(True)

    contextual = await plugin.model.economics.find_first_or_create(str(context.user.id))

    _item = contextual.partial.item

    description = "\n".join(
        [
            f"{context.emoji.berry} Ягоды: `{context.humanize(contextual.partial.berry)}`",  # noqa: E501
            f"{context.emoji.fox} Лисы: `{context.humanize(contextual.partial.fox)}`",  # noqa: E501
            f"📊 Репутация: `{context.humanize(contextual.partial.reputation)}`",
        ]
    )

    if _item:
        description += f"\n✨ Предмет: `{plugin.model.economics.shop.get(_item).label}`"

    await context.respond(
        ephemeral=True,
        embed=context.embed(
            "default",
            description=description,
        ),
    )
