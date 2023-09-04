import random

import hikari

from bot.common import plugins
from bot.common.command import commands, contexts, exceptions, options

from . import _groups, _periods

plugin = plugins.Plugin()


@plugin.include
@commands.command(
    "отобрать",
    description="Отобрать ягоды",
    period=_periods.period,
    group=_groups.group,
    options=[
        options.option(
            hikari.User,
            name="пользователь",
            description="Пользователь",
        ),
    ],
)
async def cull(
    context: contexts.Context,
    user: hikari.User,
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
        await context.handle(exceptions.NothingToCullException)

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
