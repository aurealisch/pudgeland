import random

import hikari

from trevigiano.client import plugin

from .constants import groups, periods

PLUGIN = plugin.Plugin()

COMMAND = PLUGIN.command
CONTEXT = PLUGIN.context
OPTION = PLUGIN.option


@COMMAND.command(
    PLUGIN,
    name="украсть",
    description="Украсть",
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
    EMOJI = context.emoji
    EMBED = context.embed
    HUMANIZE = context.humanize

    _CONTEXTUAL = str(context.user.id)
    _OPTIONAL = str(user.id)

    CONTEXTUAL = await PLUGIN.model.database.find(_CONTEXTUAL)
    OPTIONAL = await PLUGIN.model.database.find(_OPTIONAL)

    STEAL = PLUGIN.model.configuration.plugins.steal

    FRACTION = STEAL.fraction
    PROBABILITY = STEAL.probability

    STEALING = round((OPTIONAL.partial.berry / 2) * FRACTION)

    if STEALING < 1:
        raise Exception("Нечего красть")

    if random.choice(range(1, PROBABILITY)) != 1:
        await CONTEXTUAL.berry.remove(STEALING)

        await context.respond(
            embed=EMBED.embed(
                "default",
                description=f"""\
                    Вы попытались украсть {EMOJI.Emoji.BERRY} ягоды у <@{_OPTIONAL}>
                    и...

                    {EMOJI.Emoji.UNAVAILABLE} Не получилось...

                    ```diff\n- {HUMANIZE.humanize(STEALING)} ягод```
                """,  # noqa: E501
            )
        )

        return

    await CONTEXTUAL.berry.add(STEALING)
    await OPTIONAL.berry.remove(STEALING)

    await context.respond(
        embed=EMBED.embed(
            "default",
            description=f"""\
                Вы попытались украсть {EMOJI.Emoji.BERRY} ягоды у <@{_OPTIONAL}>
                и...

                {EMOJI.Emoji.AVAILABLE} Получилось!!!

                ```diff\n+ {HUMANIZE.humanize(STEALING)} ягод```
            """,  # noqa: E501
        )
    )


plugin = PLUGIN
