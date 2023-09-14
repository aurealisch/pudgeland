import string

from trevigiano.client import plugins

from .common import emojis, groups, periods

plugin = plugins.Plugin()

commands = plugin.commands
contexts = plugin.contexts


@commands.command(
  plugin,
  name='репутация',
  description='Репутация',
  period=periods.period,
  group=groups.group,
)
async def callback(context: 'contexts.Context') -> None:
  embeds = context.embeds
  humanizes = context.humanizes

  embed = embeds.embed
  humanize = humanizes.humanize

  users = await plugin.model.database.leaders(
    plugin.model.configuration.leaders.take,
    user_keys='reputation',
    sort_order=plugin.model.configuration.leaders.sort.order,
  )

  embed = embed('default')

  for index, user in enumerate(users):
    name = string.whitespace

    position = index + 1

    if position in emojis.emoji:
      name += emojis.emoji[position]

    name += f'#{position}'

    embed.add_field(
      name=name,
      value='\n'.join([
        f'<@{user.partial.id}>',
        f'Репутация: `{humanize(user.partial.reputation)}`',
      ]),
    )

  await context.respond(embed=embed)
