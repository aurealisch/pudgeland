import hikari

from bot.common import plugins

from ._groups import group
from ._periods import period

plugin = plugins.Plugin()


@plugin.include
@plugin.commands.command(
    "повысить",
    description="Повысить",
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
async def callback(
    context: plugin.contexts.Context,
    user: "hikari.User",
) -> None:
    await context.defer()

    contextual = str(context.user.id)
    optional = str(user.id)

    if contextual != optional:
        user = await plugin.model.economics.find_first_or_create(optional)

        await user.reputation.add(1)

        await context.respond(
            embed=context.embed(
                "default",
                description=f"📈 <@{contextual}> повысил репутацию <@{optional}>",
            ),
        )

        return

    raise plugin.exceptions.YouCantDoThatException
