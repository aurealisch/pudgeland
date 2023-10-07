from trevigiano import plugins

from .constants import periods

plugins = plugins.Plugin()

commands = plugins.commands
contexts = plugins.contexts


@plugins.include
@commands.command('профиль',
                 description='Профиль',
                 period=periods.PERIOD,
                 )
async def callback(context: contexts.Context) -> None:
    decorate = context.decorate
    embed = context.embed
    emoji = context.emoji
    humanize = context.humanize

    user = await plugins.model.database.upsert(str(context.user.id))

    description = f"""
        {emoji.Emoji.BERRY} Ягоды: {decorate.decorate(humanize.humanize(user.berry))}
        {emoji.Emoji.FOX} Лисы: {decorate.decorate(humanize.humanize(user.fox))}
        {emoji.Emoji.REPUTATION} Репутация: {decorate.decorate(humanize.humanize(user.reputation))}
    """

    await context.respond(embed=embed.embed('default', description=description))
