import crescent

from trevigiano import plugins

from ..constants import groups, periods

plugin = plugins.Plugin()

commands = plugin.commands
contexts = plugin.contexts

subGroup = crescent.SubGroup('незеритовых', groups.group, 'Незеритовых')


@plugin.include
@commands.command('ломов',
                  description='Лидеры незеритовых ломов',
                  period=periods.period,
                  group=groups.group,
                  subGroup=subGroup)
class Command(commands.Command):

    async def call(self, context: contexts.Context) -> None:
        """Description
        
        Parameters
        ----------
        context : contexts.Context
            Description
        """
        emoji = context.emoji

        users = await plugin.model.database.selectLeaders('netheriteScrap')

        _embed = context.embed.embed('netheriteScraps')

        emojis = {
            1: emoji.Emoji.first,
            2: emoji.Emoji.second,
            3: emoji.Emoji.third
        }

        for index, user in enumerate(users):
            name = '\u0020'

            position = index + 1

            if position in emojis:
                name += emojis[position]

            name += f'#{position}'

            _embed.add_field(
                name=name,
                value='\n'.join([
                    f'<@{user.id}>',
                    f'Незеритовых ломов: {context.decorate.decorate(context.humanize.humanize(user.netheriteScrap))}'  # noqa: E501
                ]))

        await context.respond(embed=_embed)
