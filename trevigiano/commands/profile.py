from trevigiano import plugin

from .constants import periods

plugin = plugin.Plugin()

cooldown = plugin.coolDown
command = plugin.command
context = plugin.context


@plugin.include
@command.command('профиль',
                 description='Профиль',
                 period=periods.PERIOD,
                 )
async def callback(context: context.Context) -> None:
    decorate = context.decorate
    embed = context.embed
    emoji = context.emoji
    humanize = context.humanize

    user = await plugin.model.database.upsert(str(context.user.id))

    description = f"""
        {emoji.Emoji.BERRY} Ягоды: {decorate.decorate(humanize.humanize(user.berry))}
        {emoji.Emoji.FOX} Лисы: {decorate.decorate(humanize.humanize(user.fox))}
        {emoji.Emoji.REPUTATION} Репутация: {decorate.decorate(humanize.humanize(user.reputation))}
    """

    await context.respond(embed=embed.embed("default", description=description))
