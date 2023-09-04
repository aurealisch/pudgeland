import hikari

from bot.common import plugins
from bot.common.command import commands, contexts, exceptions, options

from . import _groups, _periods

plugin = plugins.Plugin()


@plugin.include
@commands.command(
    "дать",
    description="Дать ягоды",
    period=_periods.period,
    group=_groups.group,
    options=[
        options.option(
            hikari.User,
            name="пользователь",
            description="Пользователь",
        ),
        options.option(
            int,
            name="количество",
            description="Количество",
        ),
    ],
)
async def give(
    context: contexts.Context,
    user: hikari.User,
    amount: int,
) -> None:
    if amount > 0:
        await context.defer()

        _optional = str(user.id)
        _contextual = str(context.user.id)

        optional = await plugin.model.economics.find_first_or_create(_optional)
        contextual = await plugin.model.economics.find_first_or_create(_contextual)

        await optional.berry.add(amount)
        await contextual.berry.remove(amount)

        await context.respond(
            embed=context.embed(
                "default",
                description=f"""\
                    <@{_contextual}> дал {context.emoji.berry} `{amount}` ягод <@{_optional}>
                """,  # noqa: E501
            ),
        )

        return

    await context.handle(exceptions.YouCantDoThatException)
