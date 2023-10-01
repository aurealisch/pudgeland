from trevigiano.client import plugin

from .constants import periods

PLUGIN = plugin.Plugin()

COMMAND = PLUGIN.command
CONTEXT = PLUGIN.context


@COMMAND.command(
    PLUGIN,
    name="профиль",
    description="Профиль",
    period=periods.PERIOD,
)
async def callback(context: "CONTEXT.Context") -> None:
    DECORATE = context.decorate
    EMBED = context.embed
    EMOJI = context.emoji
    HUMANIZE = context.humanize

    CONTEXTUAL = await PLUGIN.model.database.find(str(context.user.id))

    multiline = [
        f"{EMOJI.Emoji.BERRY} Ягоды: {DECORATE.decorate(HUMANIZE.humanize(CONTEXTUAL.partial.berry))}",  # noqa: E501
        f"{EMOJI.Emoji.FOX} Лисы: {DECORATE.decorate(HUMANIZE.humanize(CONTEXTUAL.partial.fox))}",  # noqa: E501
        f"{EMOJI.Emoji.REPUTATION} Репутация: {DECORATE.decorate(HUMANIZE.humanize(CONTEXTUAL.partial.reputation))}",  # noqa: E501
    ]

    _ITEM = CONTEXTUAL.partial.item

    if _ITEM:
        ITEM = PLUGIN.model.database.shop.get(_ITEM)

        multiline.extend([f"✨ Предмет: 🏷 Этикетка: `{ITEM.label}`"])

    DESCRIPTION = "\n".join(multiline)

    await context.respond(embed=EMBED.embed("default", description=DESCRIPTION))


plugin = PLUGIN
