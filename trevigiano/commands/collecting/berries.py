import datetime
import random

import crescent

from trevigiano import plugins

plugin = plugins.Plugin()

commands = plugin.commands
contexts = plugin.contexts

period = datetime.timedelta(hours=1, minutes=30)

group = crescent.Group('сбор', description='Сбор')


@plugin.include
@commands.command('ягод', description='Сбор ягод', period=period, group=group)
class Command(commands.Command):

    async def call(self, context: contexts.Context) -> None:
        """Description
        
        Parameters
        ----------
        context : contexts.Context
            Description
        """
        database = plugin.model.database

        decorate = context.decorate
        emoji = context.emoji
        humanize = context.humanize

        id_ = context.user.id

        user = await database.upsert(id_)

        range_ = plugin.model.configuration.get('plugins').get('collect').get(
            'range')

        berryEmoji = emoji.Emoji.berry
        foxEmoji = emoji.Emoji.fox

        foxQuantity = user.fox

        berryQuantity = sum([
            random.choice(range(range_.get('start'), range_.get('stop')))
            for _ in range(foxQuantity)
        ])

        description = f'Вы собрали {berryEmoji} {decorate.decorate(humanize.humanize(berryQuantity))} ягод от {foxEmoji} {decorate.decorate(humanize.humanize(foxQuantity))} лис'  # noqa: E501

        await database.increment(id_, 'berry', berryQuantity)

        await context.respond(
            embed=context.embed.embed('default', description=description))
