import random

from trevigiano import plugins

from .constants import groups, periods

plugin = plugins.Plugin()

commands = plugin.commands
contexts = plugin.contexts


@plugin.include
@commands.command('собрать',
                  description='Собрать',
                  period=periods.period,
                  group=groups.group)
class Command(commands.Command):

    async def call(self, context: contexts.Context) -> None:
        """Description
        
        Parameters
        ----------
        context : contexts.Context
            Description
        """
        economics = plugin.model.economics

        decorate = context.decorate
        emoji = context.emoji
        humanize = context.humanize

        id_ = context.user.id

        user = await economics.upsert(id_)

        range_ = plugin.model.configuration.get('plugins').get('collect').get(
            'range')

        fox = user.fox

        collecting = round(
            fox *
            random.choice(range(range_.get('start'), range_.get('stop'))))

        description = f'Вы собрали {emoji.Emoji.BERRY} {decorate.decorate(humanize.humanize(collecting))} ягод от {emoji.Emoji.FOX} {decorate.decorate(humanize.humanize(fox))} лис'  # noqa: E501

        await economics.increment(id_, field='berry', by=collecting)

        await context.respond(
            embed=context.embed.embed('default', description=description))
