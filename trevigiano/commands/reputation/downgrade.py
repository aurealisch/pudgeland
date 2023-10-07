import hikari

from trevigiano import plugin

from .constants import groups, periods

plugin = plugin.Plugin()

cooldown = plugin.coolDown
command = plugin.command
context = plugin.context
option = plugin.option
exceptions = plugin.exceptions


@plugin.include
@command.command('понизить',
                 description='Понизить',
                 period=periods.PERIOD,
                 group=groups.GROUP,
                 options=[option.Option(hikari.User,
                                        name='пользователь',
                                        description='Пользователь',
                                        )
                         ],
                 )
async def callback(context: context.Context, user: hikari.User) -> None:
    embed = context.embed
    emoji = context.emoji

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

    description = f'{emoji.Emoji.DOWNGRADE} Вы понизили репутацию <@{optional}>'

    await context.respond(embed=embed.embed('default', description=description))
