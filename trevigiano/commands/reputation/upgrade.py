import hikari

from trevigiano import plugin

from .constants import groups, periods

PLUGIN = plugin.Plugin()

COMMAND = PLUGIN.command
CONTEXT = PLUGIN.context
OPTION = PLUGIN.option
EXCEPTIONS = PLUGIN.exceptions


@COMMAND.command(
    PLUGIN,
    name="повысить",
    description="Повысить",
    period=periods.PERIOD,
    group=groups.GROUP,
    # fmt: off
    options=[OPTION.Option(
        hikari.User,
        name="пользователь",
        description="Пользователь",
    )],
    # fmt: on
)
async def callback(context: "CONTEXT.Context", user: "hikari.User") -> None:
    EMBED = context.embed
    EMOJI = context.emoji

    CONTEXTUAL = str(context.user.id)
    OPTIONAL = str(user.id)

    if CONTEXTUAL == OPTIONAL:
        raise EXCEPTIONS.YouCantDoThatException

    await PLUGIN.model.database.find(OPTIONAL).reputation.add(1)

    DESCRIPTION = f"{EMOJI.Emoji.UPGRADE} Вы повысили репутацию <@{OPTIONAL}>"

    await context.respond(embed=EMBED.embed("default", description=DESCRIPTION))


plugin = PLUGIN
