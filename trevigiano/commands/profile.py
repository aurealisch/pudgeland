from trevigiano import plugins

from .constants import periods

plugin = plugins.Plugin()

commands = plugin.commands
contexts = plugin.contexts


@plugin.include
@commands.command('профиль', description='Профиль', period=periods.period)
class Command(commands.Command):

    async def call(self, context: contexts.Context) -> None:
        decorate = context.decorate
        emoji = context.emoji
        humanize = context.humanize

        user = await plugin.model.economics.upsert(context.user.id)

        description = context.trim.trim(f"""
            {emoji.Emoji.BERRY} Ягоды: {decorate.decorate(humanize.humanize(user.berry))}
            {emoji.Emoji.FOX} Лисы: {decorate.decorate(humanize.humanize(user.fox))}
        """)  # noqa: E501

        await context.respond(
            embed=context.embed.embed('default', description=description))
