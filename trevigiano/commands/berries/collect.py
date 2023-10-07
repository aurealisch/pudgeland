import random

from trevigiano import plugin

from .constants import groups, periods

plugin = plugin.Plugin()

cooldown = plugin.coolDown
command = plugin.command
context = plugin.context


@plugin.include
@command.command('собрать',
                 description='Собрать',
                 period=periods.PERIOD,
                 group=groups.GROUP,
                 )
async def callback(context: context.Context) -> None:
    database = plugin.model.database

    decorate = context.decorate
    emoji = context.emoji
    embed = context.embed
    humanize = context.humanize

    id_ = str(context.user.id)

    user = await database.upsert(id_)

    fox = user.fox

    collect = plugin.model.configuration.get('plugins').get('collect')

    total = 0

    berrying = round(random.choice(range(
        collect.get('berry').get('start'),
        collect.get('berry').get('stop'),
    )))

    total += berrying

    description = f'Вы собрали {emoji.Emoji.BERRY} {decorate.decorate(humanize.humanize(berrying))} ягод'  # noqa: E501

    if fox:
        foxying = round(fox * random.choice(range(
            collect.get('fox').get('start'),
            collect.get('fox').get('stop'),
        )))

        total += foxying

        description += f'\n+ {emoji.Emoji.BERRY} {decorate.decorate(humanize.humanize(foxying))} ягод от {emoji.Emoji.FOX} {decorate.decorate(humanize.humanize(fox))} лис'  # noqa: E501
        description += f'\n\n{emoji.Emoji.TOTAL} Всего: {emoji.Emoji.BERRY} {decorate.decorate(humanize.humanize(total))} ягод'  # noqa: E501

    await database.increase(id_,
                            field='berry',
                            value=total,
                            )

    await context.respond(embed=embed.embed('default', description=description))
