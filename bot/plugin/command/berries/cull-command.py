import random

import hikari

from bot.common import plugins

from ._groups import group
from ._periods import period

plugin = plugins.Plugin()


@plugin.include
@plugin.commands.command(
    "отобрать",
    description="Отобрать ягоды",
    period=period,
    group=group,
    options=[
        plugin.options.option(
            hikari.User,
            name="пользователь",
            description="Пользователь",
        ),
    ],
)
async def cull(
    context: plugin.contexts.Context,
    user: "hikari.User",
) -> None:
    await context.defer()

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
        random.choice(
            range(
                1,
                cull.edge,
            )
        )
        != 1
    ):
        await contextual.berry.remove(culling)

        await context.respond(
            embed=context.embed(
                "default",
                description=f"""\
                    <@{_contextual}> попытался отобрать {context.emoji.berry} ягоды у <@{_optional}>
                    и...

                    ❌ Не получилось...

                    ```diff\n- {context.humanize(culling)} ягод```
                """,  # noqa: E501
            ),
        )

        return

    await contextual.berry.add(culling)
    await optional.berry.remove(culling)

    await context.respond(
        embed=context.embed(
            "default",
            description=f"""\
                <@{_contextual}> попытался отобрать {context.emoji.berry} ягоды у <@{_optional}>
                и...

                ✅ Получилось!!!

                ```diff\n+ {context.humanize(culling)} ягод```
            """,  # noqa: E501
        ),
    )
