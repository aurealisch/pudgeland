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
    name="подарить",
    description="Подарить",
    period=periods.PERIOD,
    group=groups.GROUP,
    options=[
        OPTIONS.Option(
            hikari.User,
            name="пользователь",
            description="Пользователь",
        ),
        OPTIONS.Option(
            int,
            name="количество",
            description="Количество",
        ),
    ],
)
async def callback(
    context: "CONTEXTS.Context",
    user: "hikari.User",
    amount: int,
) -> None:
    if amount < 0:
        raise PLUGIN.exceptions.YouCantDoThatException

    EMOJIS = context.emojis
    EMBEDS = context.embeds
    HUMANIZES = context.humanizes

    _OPTIONAL = str(user.id)
    _CONTEXTUAL = str(context.user.id)

    OPTIONAL = await PLUGIN.model.database.find(_OPTIONAL)
    CONTEXTUAL = await PLUGIN.model.database.find(_CONTEXTUAL)

    await OPTIONAL.berry.add(amount)
    await CONTEXTUAL.berry.remove(amount)

    await context.respond(
        embed=EMBEDS.embed(
            "default",
            description=f"""\
                Вы дали {EMOJIS.Emoji.BERRY} `{HUMANIZES.humanize(amount)}` ягод <@{_OPTIONAL}>
            """,  # noqa: E501
        )
    )


plugin = PLUGIN
