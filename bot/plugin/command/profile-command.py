from bot.common import plugins, shops
from bot.common.command import commands, contexts, cooldowns

plugin = plugins.Plugin()


@plugin.include
@commands.command(
    "профиль",
    description="Профиль",
    period=cooldowns.Period(
        seconds=2,
        milliseconds=500,
    ),  # 2.5 seconds
)
async def callback(context: contexts.Context) -> None:
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
        description += f"\n✨ Предмет: `{shops.shop.get(_item).label}`"

    await context.respond(
        ephemeral=True,
        embed=context.embed(
            "default",
            description=description,
        ),
    )
