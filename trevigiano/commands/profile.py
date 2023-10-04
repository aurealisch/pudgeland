from trevigiano import plugin

from .constants import periods

PLUGIN = plugin.Plugin()

COOLDOWN = PLUGIN.coolDown
COMMAND = PLUGIN.command
CONTEXT = PLUGIN.context


@PLUGIN.include
@COMMAND.command(
    "профиль",
    description="Профиль",
    period=periods.PERIOD,
)
async def callback(context: CONTEXT.Context) -> None:
    DECORATE = context.decorate
    EMBED = context.embed
    EMOJI = context.emoji
    HUMANIZE = context.humanize

    user = await PLUGIN.model.database.selectOrInsertUser(str(context.user.id))

    multiline = [
        f"{EMOJI.Emoji.BERRY} Ягоды: {DECORATE.decorate(HUMANIZE.humanize(user.berry))}",  # noqa: E501
        f"{EMOJI.Emoji.FOX} Лисы: {DECORATE.decorate(HUMANIZE.humanize(user.fox))}",  # noqa: E501
        f"{EMOJI.Emoji.REPUTATION} Репутация: {DECORATE.decorate(HUMANIZE.humanize(user.reputation))}",  # noqa: E501
    ]

    DESCRIPTION = "\n".join(multiline)

    await context.respond(embed=EMBED.embed("default", description=DESCRIPTION))


plugin = PLUGIN
