import random

import hikari

from bot.common import plugins

from ._groups import group
from ._periods import period

plugin = plugins.Plugin()

commands = plugin.commands
contexts = plugin.contexts
options = plugin.options


@commands.command(
    plugin,
    name="отобрать",
    description="Отобрать ягоды",
    period=period,
    group=group,
    options=[
        options.option(
            hikari.User,
            name="пользователь",
            description="Пользователь",
        ),
    ],
)
async def callback(
    context: contexts.Context,
    user: "hikari.User",
) -> None:
    _ = context.humanize

    _contextual = str(context.user.id)
    _optional = str(user.id)

    contextual = await plugin.model.economics.find_first_or_create(_contextual)
    optional = await plugin.model.economics.find_first_or_create(_optional)

    cull = plugin.model.configuration.plugins.cull

    fraction = cull.fraction

    culling = round((optional.partial.berry / 2) * fraction)

    if culling < 1:
        raise Exception("Нечего отбирать")

    if (
        # fmt: off
        random.choice(range(
            1,
            cull.edge,
        ))
        # fmt: on
        != 1
    ):
        await contextual.berry.remove(culling)

        # fmt: off
        await context.respond(embed=context.embed(
            "default",
            description=f"""\
                Вы попытались отобрать {context.emoji.berry} ягоды у <@{_optional}>
                и...

                ❌ Не получилось...

                ```diff\n- {_(culling)} ягод```
            """,  # noqa: E501
        ))
        # fmt: on

        return

    await contextual.berry.add(culling)
    await optional.berry.remove(culling)

    # fmt: off
    await context.respond(embed=context.embed(
        "default",
        description=f"""\
            Вы попытались отобрать {context.emoji.berry} ягоды у <@{_optional}>
            и...

            ✅ Получилось!!!

            ```diff\n+ {_(culling)} ягод```
        """,  # noqa: E501
    ))
    # fmt: on
