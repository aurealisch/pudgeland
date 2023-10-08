import hikari

from trevigiano import plugins

from .constants import groups, periods

plugin = plugins.Plugin()

commands = plugin.commands
contexts = plugin.contexts
options = plugin.options
exceptions = plugin.exceptions


@plugin.include
@commands.command('понизить',
                  description='Понизить',
                  period=periods.PERIOD,
                  group=groups.GROUP,
                  options=[options.Option(hikari.User,
                                          name='пользователь',
                                          description='Пользователь')],
                  )
async def callback(context: contexts.Context, user: hikari.User) -> None:
    contextual = str(context.user.id)
    optional = str(user.id)

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
