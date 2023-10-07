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
@command.command('повысить',
                 description='Повысить',
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

    await plugin.model.database.increase(optional,
                                         field='reputation',
                                         value=1,
                                         )

    DESCRIPTION = f'{emoji.Emoji.UPGRADE} Вы повысили репутацию <@{optional}>'

    await context.respond(embed=embed.embed('default', description=DESCRIPTION))
