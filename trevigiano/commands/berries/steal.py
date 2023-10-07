import random

import hikari

from trevigiano import plugins

from .constants import groups, periods

plugin = plugins.Plugin()

commands = plugin.commands
contexts = plugin.contexts
options = plugin.options


@plugin.include
@commands.command('украсть',
                  description='Украсть',
                  period=periods.PERIOD,
                  group=groups.GROUP,
                  options=[options.Option(hikari.User,
                                          name='пользователь',
                                          description='Пользователь')],
                  )
async def callback(context: contexts.Context, user: hikari.User) -> None:
    database = plugin.model.database

    emoji = context.emoji
    embed = context.embed
    humanize = context.humanize
    trim = context.trim

    _contextual = str(context.user.id)
    _optional = str(user.id)

    optional = await database.upsert(_optional)

    steal = plugin.model.configuration.get('plugins').get('steal')

    fraction = steal.get('fraction')
    probability = steal.get('probability')

    stealing = round((optional.berry / 2) * fraction)

    if stealing < 1:
        raise Exception('Нечего красть')

    if random.choice(range(1, probability)) != 1:
        await database.decrease(_contextual,
                                field='berry',
                                value=stealing,
                                )

        description = trim.trim(
            f"""\
                Вы попытались украсть {emoji.Emoji.BERRY} ягоды у <@{_optional}>
                и...

                {emoji.Emoji.UNAVAILABLE} Не получилось...

                ```diff\n- {humanize.humanize(stealing)} ягод```
            """  # noqa: E501
        )

        await context.respond(embed=embed.embed('default', description=description))

        return

    await database.increase(_contextual,
                            field='berry',
                            value=stealing,
                            )
    await database.decrease(_optional,
                            field='berry',
                            value=stealing,
                            )

    description = trim.trim(
        f"""\
            Вы попытались украсть {emoji.Emoji.BERRY} ягоды у <@{_optional}>
            и...

            {emoji.Emoji.AVAILABLE} Получилось!!!

            ```diff\n+ {humanize.humanize(stealing)} ягод```
        """  # noqa: E501
    )

    await context.respond(embed=embed.embed('default', description=description))
