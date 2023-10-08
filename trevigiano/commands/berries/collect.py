import random

from trevigiano import plugins

from .constants import groups, periods

plugin = plugins.Plugin()

commands = plugin.commands
contexts = plugin.contexts


@plugin.include
@commands.command('собрать',
                  description='Собрать',
                  period=periods.PERIOD,
                  group=groups.GROUP,
                  )
async def callback(context: contexts.Context) -> None:
    database = plugin.model.database

    decorate = context.decorate
    emoji = context.emoji
    humanize = context.humanize

    id_ = str(context.user.id)

    user = await database.upsert(id_)

    range_ = plugin.model.configuration.get('plugins').get('collect').get('range')

    fox = user.fox

    collecting = round(fox * random.choice(range(
        range_.get('start'),
        range_.get('stop'),
    )))

    description = f'Вы собрали {emoji.Emoji.BERRY} {decorate.decorate(humanize.humanize(collecting))} ягод от {emoji.Emoji.FOX} {decorate.decorate(humanize.humanize(fox))} лис'

    await database.increase(id_,
                            field='berry',
                            value=collecting,
                            )

    await context.respond(embed=context.embed.embed('default', description=description))
