import random

import hikari
import crescent

from trevigiano import plugins

from .constants import groups, periods

plugin = plugins.Plugin()

commands = plugin.commands
contexts = plugin.contexts
errors = plugin.errors


@plugin.include
@commands.command('украсть',
                  description='Украсть',
                  period=periods.period,
                  group=groups.group)
class Command(commands.Command):
    user = crescent.option(hikari.User,
                           name='пользователь',
                           description='Пользователь')

    async def call(self, context: contexts.Context) -> None:
        """Description
        
        Parameters
        ----------
        context : contexts.Context
            Description
        """
        database = plugin.model.database

        emoji = context.emoji
        embed = context.embed
        humanize = context.humanize
        trim = context.trim

        _contextual = context.user.id
        _optional = self.user.id

        optional = await database.upsert(_optional)

        steal = plugin.model.configuration.get('plugins').get('steal')

        fraction = steal.get('fraction')
        probability = steal.get('probability')

        stealing = round((optional.berry / 2) * fraction)

        if stealing < 1:
            raise errors.Error('Нечего красть')

        if random.choice(range(1, probability)) != 1:
            await database.decrease(_contextual, field='berry', value=stealing)

            description = trim.trim(f"""\
                Вы попытались украсть {emoji.Emoji.BERRY} ягоды у <@{_optional}>
                и...

                {emoji.Emoji.UNAVAILABLE} Не получилось...

                ```diff\n- {humanize.humanize(stealing)} ягод```
            """)

            await context.respond(
                embed=embed.embed('default', description=description))

            return

        await database.increment(_contextual, field='berry', by=stealing)
        await database.decrement(_optional, field='berry', by=stealing)

        description = trim.trim(f"""\
            Вы попытались украсть {emoji.Emoji.BERRY} ягоды у <@{_optional}>
            и...

            {emoji.Emoji.AVAILABLE} Получилось!!!

            ```diff\n+ {humanize.humanize(stealing)} ягод```
        """)

        await context.respond(
            embed=embed.embed('default', description=description))
