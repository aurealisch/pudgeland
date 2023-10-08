from trevigiano import plugins

from .constants import periods

plugin = plugins.Plugin()

commands = plugin.commands
contexts = plugin.contexts


@plugin.include
@commands.command('профиль',
                  description='Профиль',
                  period=periods.PERIOD,
                  )
async def callback(context: contexts.Context) -> None:
    decorate = context.decorate
    emoji = context.emoji
    humanize = context.humanize

    user = await plugin.model.database.upsert(str(context.user.id))

    description = context.trim.trim(
        f"""
            {emoji.Emoji.BERRY} Ягоды: {decorate.decorate(humanize.humanize(user.berry))}
            {emoji.Emoji.FOX} Лисы: {decorate.decorate(humanize.humanize(user.fox))}
            {emoji.Emoji.REPUTATION} Репутация: {decorate.decorate(humanize.humanize(user.reputation))}
        """
    )

    await context.respond(embed=context.embed.embed('default', description=description))
