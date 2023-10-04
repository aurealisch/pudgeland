from trevigiano import plugin

from .constants import groups, periods

PLUGIN = plugin.Plugin()

COOLDOWN = PLUGIN.coolDown
COMMAND = PLUGIN.command
CONTEXT = PLUGIN.context


@PLUGIN.include
@COMMAND.command(
    "лисы",
    description="Лисы",
    period=periods.PERIOD,
    group=groups.GROUP,
)
async def callback(context: CONTEXT.Context) -> None:
    DECORATE = context.decorate
    EMBED = context.embed
    EMOJI = context.emoji
    HUMANIZE = context.humanize

    USERS = await PLUGIN.model.database.selectLeaders("fox")

    _EMBED = EMBED.embed("default")

    EMOJIS = {
        1: EMOJI.Emoji.FIRST_PLACE,
        2: EMOJI.Emoji.SECOND_PLACE,
        3: EMOJI.Emoji.THIRD_PLACE,
    }

    for INDEX, USER in enumerate(USERS):
        name = "\u0020"

        POSITION = INDEX + 1

        if POSITION in EMOJIS:
            name += EMOJIS[POSITION]

        name += f"#{POSITION}"

        _EMBED.add_field(
            name=name,
            # fmt: off
            value="\n".join([
                f"<@{USER.id}>",
                f"Лисы: {DECORATE.decorate(HUMANIZE.humanize(USER.fox))}",
            ])
            # fmt: on
        )

    await context.respond(embed=_EMBED)


plugin = PLUGIN
