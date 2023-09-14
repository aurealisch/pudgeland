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
  name='подарить',
  description='Подарить',
  period=periods.period,
  group=groups.group,
  options=[
    options.Option(
      hikari.User,
      name='пользователь',
      description='Пользователь',
    ),
    options.Option(
      int,
      name='количество',
      description='Количество',
    ),
  ],
)
async def callback(
  context: 'contexts.Context',
  user: 'hikari.User',
  amount: int,
) -> None:
  if amount < 0:
    raise plugin.exceptions.YouCantDoThatException
  
  embeds = context.embeds
  humanizes = context.humanizes

  embed = embeds.embed
  humanize = humanizes.humanize

  _optional = str(user.id)
  _contextual = str(context.user.id)

  optional = await plugin.model.database.find(_optional)
  contextual = await plugin.model.database.find(_contextual)

  await optional.berry.add(amount)
  await contextual.berry.remove(amount)

  await context.respond(embed=embed(
    'default',
    description=f"""\
      Вы дали {context.emoji.berry} `{humanize(amount)}` ягод <@{_optional}>
    """,  # noqa: E501
  ))
