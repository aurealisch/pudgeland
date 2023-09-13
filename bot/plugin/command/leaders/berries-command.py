import string

from bot.common import plugins

from ._emojis import emoji
from ._groups import group
from ._periods import period

plugin = plugins.Plugin()

commands = plugin.commands
contexts = plugin.contexts


@commands.command(
  plugin,
  name='ягоды',
  description='Лидеры по ягодам',
  period=period,
  group=group,
)
async def callback(context: contexts.Context) -> None:
  _ = context.humanize

  users = await plugin.model.economics.find_many(
    plugin.model.configuration.leaders.take,
    user_keys='berry',
    sort_order=plugin.model.configuration.leaders.sort.order,
  )

  embed = context.embed('default')

  for index, user in enumerate(users):
    name = string.whitespace

    position = index + 1

    if position in emoji:
      name += emoji[position]

    name += f'#{position}'

    embed.add_field(
      name=name,
      value='\n'.join([
        f'<@{user.partial.id}>',
        f'Ягоды: `{_(user.partial.berry)}`',
      ]),
    )

  await context.respond(embed=embed)
