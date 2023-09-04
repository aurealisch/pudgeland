import hikari

from bot.common import plugins
from bot.common.command import commands, contexts, exceptions, options

from . import _groups, _periods

plugin = plugins.Plugin()


@plugin.include
@commands.command(
    "понизить",
    description="Понизить",
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
async def callback(
    context: contexts.Context,
    user: hikari.User,
) -> None:
    await context.defer()

    contextual = str(context.user.id)
    optional = str(user.id)

    if contextual != optional:
        user = await plugin.model.economics.find_first_or_create(optional)

        await user.reputation.remove(1)

        await context.respond(
            embed=context.embed(
                "default",
                description=f"📉 <@{contextual}> понизил репутацию <@{optional}>",
            ),
        )

        return

    await context.handle(exceptions.YouCantDoThatException)
