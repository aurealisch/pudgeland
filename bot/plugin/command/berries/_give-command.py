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
  name='дать',
  description='Дать ягоды',
  period=period,
  group=group,
  options=[
    options.option(
      hikari.User,
      name='пользователь',
      description='Пользователь',
    ),
    options.option(
      int,
      name='количество',
      description='Количество',
    ),
  ],
)
async def callback(
  context: contexts.Context,
  user: 'hikari.User',
  amount: int,
) -> None:
  if amount > 0:
    _ = context.humanize

    _optional = str(user.id)
    _contextual = str(context.user.id)

    optional = await plugin.model.economics.find_first_or_create(_optional)
    contextual = await plugin.model.economics.find_first_or_create(_contextual)

    await optional.berry.add(amount)
    await contextual.berry.remove(amount)

    await context.respond(embed=context.embed(
      'default',
      description=f"""\
        Вы дали {context.emoji.berry} `{_(amount)}` ягод <@{_optional}>
      """,  # noqa: E501
    ))

    return

  raise plugin.exceptions.YouCantDoThatException
