from trevigiano.client import plugins

from .constants import periods

PLUGIN = plugins.Plugin()

COMMANDS = PLUGIN.commands
CONTEXTS = PLUGIN.contexts


@COMMANDS.command(
    PLUGIN,
    name="профиль",
    description="Профиль",
    period=periods.PERIOD,
)
async def callback(context: "CONTEXTS.Context") -> None:
    EMBEDS = context.embeds
    EMOJIS = context.emojis
    HUMANIZES = context.humanizes

    CONTEXTUAL = await PLUGIN.model.database.find(str(context.user.id))

    multiline = [
        f"{EMOJIS.Emoji.BERRY} Ягоды: `{HUMANIZES.humanize(CONTEXTUAL.partial.berry)}`",  # noqa: E501
        f"{EMOJIS.Emoji.FOX} Лисы: `{HUMANIZES.humanize(CONTEXTUAL.partial.fox)}`",  # noqa: E501
        f"📊 Репутация: `{HUMANIZES.humanize(CONTEXTUAL.partial.reputation)}`",
    ]

    _ITEM = CONTEXTUAL.partial.item

    if _ITEM:
        ITEM = PLUGIN.model.database.shop.get(_ITEM)

        multiline.extend([f"✨ Предмет: 🏷 Этикетка: `{ITEM.label}`"])

    DESCRIPTION = "\n".join(multiline)

    await context.respond(embed=EMBEDS.embed("default", description=DESCRIPTION))


plugin = PLUGIN
