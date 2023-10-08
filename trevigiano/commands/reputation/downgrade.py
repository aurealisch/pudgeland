import hikari
import crescent

from trevigiano import plugins

from .constants import groups, periods

plugin = plugins.Plugin()

commands = plugin.commands
contexts = plugin.contexts
exceptions = plugin.exceptions


@plugin.include
@commands.command('понизить',
                  description='Понизить',
                  period=periods.PERIOD,
                  group=groups.GROUP,
                  )
class Command(commands.Command):
    user = crescent.option(hikari.User,
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

        await plugin.model.database.decrease(optional,
                                            field='reputation',
                                            value=1,
                                            )

        description = f'{context.emoji.Emoji.DOWNGRADE} Вы понизили репутацию <@{optional}>'

        await context.respond(embed=context.embed.embed('default', description=description))
