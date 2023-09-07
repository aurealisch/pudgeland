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
    name="повысить",
    description="Повысить репутацию пользователю",
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
    contextual = str(context.user.id)
    optional = str(user.id)

    if contextual != optional:
        user = await plugin.model.economics.find_first_or_create(optional)

        await user.reputation.add(1)

        # fmt: off
        await context.respond(embed=context.embed(
            "default",
            description=f"📈 Вы повысили репутацию <@{optional}>",
        ))
        # fmt: on

        return

    raise plugin.exceptions.YouCantDoThatException
