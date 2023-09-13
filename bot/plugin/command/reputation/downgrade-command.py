import hikari

from bot.common import plugins

from ._groups import group
from ._periods import period

plugin = plugins.Plugin()

commands = plugin.commands
contexts = plugin.contexts
options = plugin.options


@commands.command(
  plugin,
  name='понизить',
  description='Понизить репутацию пользователю',
  period=period,
  group=group,
  options=[
    options.option(
      hikari.User,
      name='пользователь',
      description='Пользователь',
    ),
  ],
)
async def callback(
  context: contexts.Context,
  user: 'hikari.User',
) -> None:
  contextual = str(context.user.id)
  optional = str(user.id)

  if contextual != optional:
    user = await plugin.model.economics.find_first_or_create(optional)

    await user.reputation.remove(1)

    await context.respond(embed=context.embed(
      'default',
      description=f'📉 Вы понизили репутацию <@{optional}>',
    ))

    return

  raise plugin.exceptions.YouCantDoThatException
