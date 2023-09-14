from trevigiano.client import plugins

from .common import periods

plugin = plugins.Plugin()

commands = plugin.commands
contexts = plugin.contexts


@commands.command(
  plugin,
  name='профиль',
  description='Профиль',
  period=periods.period,
)
async def callback(context: 'contexts.Context') -> None:
  contextual = await plugin.model.database.find(str(context.user.id))

  emojis = context.emojis
  embeds = context.embeds
  humanizes = context.humanizes

  emoji = emojis.Emoji
  embed = embeds.embed
  humanize = humanizes.humanize

  description = [
    f'{emoji.berry} Ягоды: `{humanize(contextual.partial.berry)}`',
    f'{emoji.fox} Лисы: `{humanize(contextual.partial.fox)}`',
    f'📊 Репутация: `{humanize(contextual.partial.reputation)}`',
  ]

  _item = contextual.partial.item

  if _item:
    description.extend([
      f'✨ Предмет: 🏷 Этикетка`{plugin.model.database.store.get(_item).label}`'
    ])

  await context.respond(embed=embed(
    'default',
    description='\n'.join(description),
  ))
