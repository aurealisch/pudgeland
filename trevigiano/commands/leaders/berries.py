from trevigiano import plugins

from .constants import groups, periods

plugin = plugins.Plugin()

commands = plugin.commands
contexts = plugin.contexts


@plugin.include
@commands.command('ягоды',
                 description='Ягоды',
                 period=periods.PERIOD,
                 group=groups.GROUP,
                 )
async def callback(context: contexts.Context) -> None:
    decorate = context.decorate
    embed = context.embed
    emoji = context.emoji
    humanize = context.humanize

    users = await plugin.model.database.selectLeaders('berry')

    _embed = embed.embed('default')

    emojis = {
        1: emoji.Emoji.FIRST_PLACE,
        2: emoji.Emoji.SECOND_PLACE,
        3: emoji.Emoji.THIRD_PLACE,
    }

    for index, user in enumerate(users):
        name = '\u0020'

        position = index + 1

        if position in emojis:
            name += emojis[position]

        name += f'#{position}'

        _embed.add_field(name=name,
                         value='\n'.join([
                             f'<@{user.id}>',
                             f'Ягоды: {decorate.decorate(humanize.humanize(user.berry))}',
                         ])
                         )

    await context.respond(embed=_embed)
