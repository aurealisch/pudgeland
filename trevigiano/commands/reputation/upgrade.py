import hikari

from trevigiano import plugins

from .constants import groups, periods

plugin = plugins.Plugin()

commands = plugin.commands
contexts = plugin.contexts
options = plugin.options
exceptions = plugin.exceptions


@plugin.include
@commands.command('повысить',
                 description='Повысить',
                 period=periods.PERIOD,
                 group=groups.GROUP,
                 options=[options.Option(hikari.User,
                                        name='пользователь',
                                        description='Пользователь',
                                        )
                         ],
                 )
async def callback(context: contexts.Context, user: hikari.User) -> None:
    embed = context.embed
    emoji = context.emoji

    contextual = str(context.user.id)
    optional = str(user.id)

    if contextual == optional:
        raise exceptions.YouCantDoThatException

    await plugin.model.database.upsert(contextual)
    await plugin.model.database.upsert(optional)

    await plugin.model.database.increase(optional,
                                         field='reputation',
                                         value=1,
                                         )

    description = f'{emoji.Emoji.UPGRADE} Вы повысили репутацию <@{optional}>'

    await context.respond(embed=embed.embed('default', description=description))
