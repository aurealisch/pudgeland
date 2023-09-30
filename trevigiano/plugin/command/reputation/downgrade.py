import hikari

from trevigiano.client import plugins

from .constants import groups, periods

PLUGIN = plugins.Plugin()

COMMANDS = PLUGIN.commands
CONTEXTS = PLUGIN.contexts
OPTIONS = PLUGIN.options
EXCEPTIONS = PLUGIN.exceptions


@COMMANDS.command(
    PLUGIN,
    name="понизить",
    description="Понизить",
    period=periods.PERIOD,
    group=groups.GROUP,
    # fmt: off
    options=[OPTIONS.Option(
        hikari.User,
        name="пользователь",
        description="Пользователь",
    )],
    # fmt: on
)
async def callback(context: "CONTEXTS.Context", user: "hikari.User") -> None:
    EMBEDS = context.embeds

    CONTEXTUAL = str(context.user.id)
    OPTIONAL = str(user.id)

    if CONTEXTUAL == OPTIONAL:
        raise EXCEPTIONS.YouCantDoThatException

    await PLUGIN.model.database.find(OPTIONAL).reputation.add(1)

    DESCRIPTION = f"📉 Вы понизили репутацию <@{OPTIONAL}>"

    await context.respond(embed=EMBEDS.embed("default", description=DESCRIPTION))


plugin = PLUGIN
