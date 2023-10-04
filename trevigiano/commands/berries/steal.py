import random

import hikari

from trevigiano import plugin

from .constants import groups, periods

PLUGIN = plugin.Plugin()

COOLDOWN = PLUGIN.coolDown
COMMAND = PLUGIN.command
CONTEXT = PLUGIN.context
OPTION = PLUGIN.option


@PLUGIN.include
@COMMAND.command(
    "украсть",
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
async def callback(context: CONTEXT.Context, user: hikari.User) -> None:
    DATABASE = PLUGIN.model.database

    EMOJI = context.emoji
    EMBED = context.embed
    HUMANIZE = context.humanize
    TRIM = context.trim

    _CONTEXTUAL = str(context.user.id)
    _OPTIONAL = str(user.id)

    OPTIONAL = await DATABASE.selectOrInsertUser(_OPTIONAL)

    STEAL = PLUGIN.model.configuration.get("plugins").get("steal")

    FRACTION = STEAL.get("fraction")
    PROBABILITY = STEAL.get("probability")

    STEALING = round((OPTIONAL.berry / 2) * FRACTION)

    if STEALING < 1:
        raise Exception("Нечего красть")

    if random.choice(range(1, PROBABILITY)) != 1:
        await DATABASE.decrease(
            _CONTEXTUAL,
            key="berry",
            value=STEALING,
        )

        await context.respond(
            embed=EMBED.embed(
                "default",
                description=TRIM.trim(
                    f"""\
                        Вы попытались украсть {EMOJI.Emoji.BERRY} ягоды у <@{_OPTIONAL}>
                        и...

                        {EMOJI.Emoji.UNAVAILABLE} Не получилось...

                        ```diff\n- {HUMANIZE.humanize(STEALING)} ягод```
                    """  # noqa: E501
                ),
            )
        )

        return

    await DATABASE.increase(
        _CONTEXTUAL,
        key="berry",
        value=STEALING,
    )
    await DATABASE.decrease(
        _OPTIONAL,
        key="berry",
        value=STEALING,
    )

    await context.respond(
        embed=EMBED.embed(
            "default",
            description=TRIM.trim(
                f"""\
                    Вы попытались украсть {EMOJI.Emoji.BERRY} ягоды у <@{_OPTIONAL}>
                    и...

                    {EMOJI.Emoji.AVAILABLE} Получилось!!!

                    ```diff\n+ {HUMANIZE.humanize(STEALING)} ягод```
                """  # noqa: E501
            ),
        )
    )


plugin = PLUGIN
