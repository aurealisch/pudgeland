import random

import hikari

from trevigiano.client import plugins

from .constants import groups, periods

PLUGIN = plugins.Plugin()

COMMANDS = PLUGIN.commands
CONTEXTS = PLUGIN.contexts
OPTIONS = PLUGIN.options


@COMMANDS.command(
    PLUGIN,
    name="украсть",
    description="Украсть",
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
    EMOJIS = context.emojis
    EMBEDS = context.embeds
    HUMANIZES = context.humanizes

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
            embed=EMBEDS.embed(
                "default",
                description=f"""\
                    Вы попытались украсть {EMOJIS.Emoji.BERRY} ягоды у <@{_OPTIONAL}>
                    и...

                    ❌ Не получилось...

                    ```diff\n- {HUMANIZES.humanize(STEALING)} ягод```
                """,  # noqa: E501
            )
        )

        return

    await CONTEXTUAL.berry.add(STEALING)
    await OPTIONAL.berry.remove(STEALING)

    await context.respond(
        embed=EMBEDS.embed(
            "default",
            description=f"""\
                Вы попытались украсть {EMOJIS.Emoji.BERRY} ягоды у <@{_OPTIONAL}>
                и...

                ✅ Получилось!!!

                ```diff\n+ {HUMANIZES.humanize(STEALING)} ягод```
            """,  # noqa: E501
        )
    )


plugin = PLUGIN
