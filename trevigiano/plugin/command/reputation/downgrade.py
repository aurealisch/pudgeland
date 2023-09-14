import hikari

from trevigiano.client import plugins

from .common import groups, periods

plugin = plugins.Plugin()

commands = plugin.commands
contexts = plugin.contexts
options = plugin.options
exceptions = plugin.exceptions


@commands.command(
  plugin,
  name='понизить',
  description='Понизить',
  period=periods.period,
  group=groups.group,
  options=[options.Option(
    hikari.User,
    name='пользователь',
    description='Пользователь',
  )],
)
async def callback(
  context: 'contexts.Context',
  user: 'hikari.User',
) -> None:
  embeds = context.embeds

  embed = embeds.embed

  contextual = str(context.user.id)
  optional = str(user.id)

  if not contextual != optional:
    raise exceptions.YouCantDoThatException

  user = await plugin.model.database.find(optional)

  await user.reputation.remove(1)

  await context.respond(embed=embed(
    'default',
    description=f'📉 Вы понизили репутацию <@{optional}>',
  ))
