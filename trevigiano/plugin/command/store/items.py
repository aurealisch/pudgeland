from trevigiano.client import plugins

from .common import groups, periods

plugin = plugins.Plugin()

commands = plugin.commands
contexts = plugin.contexts


@commands.command(
  plugin,
  name='предметы',
  description='Предметы',
  period=periods.period,
  group=groups.group,
)
async def callback(context: 'contexts.Context') -> None:
  store = plugin.model.database.store

  embeds = context.embeds
  humanizes = context.humanizes

  embed = embeds.embed
  humanize = humanizes.humanize

  description = '\n'.join([
    '\n'.join([
      f'# {item.emoji} {item.label}',
      f'> {item.description}',
      f'🏷 Цена: {context.emoji.berry} Ягоды: `{humanize(item.price)}`'
    ])
    for _, item in store.items()
  ])

  await context.respond(embed=embed(
    'default',
    description=description,
  ))
