import hikari
import crescent

from trevigiano import plugins

from .constants import groups, periods

plugin = plugins.Plugin()

commands = plugin.commands
contexts = plugin.contexts
exceptions = plugin.exceptions


@plugin.include
@commands.command(
    'повысить',
    description='Повысить',
    period=periods.PERIOD,
    group=groups.GROUP,
)
class Command(commands.Command):
    user = crescent.option(
        hikari.User,
        name='пользователь',
        description='Пользователь',
    )

    async def call(self, context: contexts.Context) -> None:
        contextual = str(context.user.id)
        optional = str(self.user.id)

        if contextual == optional:
            raise exceptions.YouCantDoThatException

        await plugin.model.database.upsert(contextual)
        await plugin.model.database.upsert(optional)

        await plugin.model.database.increase(
            optional,
            field='reputation',
            value=1,
        )

        description = f'{context.emoji.Emoji.UPGRADE} Вы повысили репутацию <@{optional}>'  # noqa: E501

        await context.respond(
            embed=context.embed.embed('default', description=description))
