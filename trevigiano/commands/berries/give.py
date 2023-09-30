import hikari

from trevigiano.client import plugin

from .constants import groups, periods

PLUGIN = plugin.Plugin()

COMMAND = PLUGIN.command
CONTEXT = PLUGIN.context
OPTION = PLUGIN.option
EXCEPTIONS = PLUGIN.exceptions


@COMMAND.command(
    PLUGIN,
    name="подарить",
    description="Подарить",
    period=periods.PERIOD,
    group=groups.GROUP,
    options=[
        OPTION.Option(
            hikari.User,
            name="пользователь",
            description="Пользователь",
        ),
        OPTION.Option(
            int,
            name="количество",
            description="Количество",
        ),
    ],
)
async def callback(
    context: "CONTEXT.Context",
    user: "hikari.User",
    amount: int,
) -> None:
    if amount < 0:
        raise PLUGIN.exceptions.YouCantDoThatException

    EMOJI = context.emoji
    EMBED = context.embed
    HUMANIZE = context.humanize

    _OPTIONAL = str(user.id)
    _CONTEXTUAL = str(context.user.id)

    OPTIONAL = await PLUGIN.model.database.find(_OPTIONAL)
    CONTEXTUAL = await PLUGIN.model.database.find(_CONTEXTUAL)

    await OPTIONAL.berry.add(amount)
    await CONTEXTUAL.berry.remove(amount)

    await context.respond(
        embed=EMBED.embed(
            "default",
            description=f"""\
                Вы дали {EMOJI.Emoji.BERRY} `{HUMANIZE.humanize(amount)}` ягод <@{_OPTIONAL}>
            """,  # noqa: E501
        )
    )


plugin = PLUGIN
