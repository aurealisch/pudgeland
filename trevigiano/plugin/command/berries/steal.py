import random

import hikari

from trevigiano.client import plugins

from .common import groups, periods

plugin = plugins.Plugin()

commands = plugin.commands
contexts = plugin.contexts
options = plugin.options


@commands.command(
  plugin,
  name='украсть',
  description='Украсть',
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
  emojis = context.emojis
  embeds = context.embeds
  humanizes = context.humanizes

  emoji = emojis.Emoji
  embed = embeds.embed
  humanize = humanizes.humanize

  _contextual = str(context.user.id)
  _optional = str(user.id)

  contextual = await plugin.model.database.find(_contextual)
  optional = await plugin.model.database.find(_optional)

  steal = plugin.model.configuration.plugins.steal

  fraction = steal.fraction
  probability = steal.probability

  stealing = round((optional.partial.berry / 2) * fraction)

  if stealing < 1:
    raise Exception('Нечего красть')

  if (random.choice(range(
    1,
    probability,
  ))) != 1:
    await contextual.berry.remove(stealing)

    await context.respond(embed=embeds.embed(
      'default',
      description=f"""\
        Вы попытались украсть {emoji.berry} ягоды у <@{_optional}>
        и...

        ❌ Не получилось...

        ```diff\n- {humanize(stealing)} ягод```
      """,  # noqa: E501
    ))

    return

  await contextual.berry.add(stealing)
  await optional.berry.remove(stealing)

  await context.respond(embed=embed(
    'default',
    description=f"""\
      Вы попытались украсть {emoji.berry} ягоды у <@{_optional}>
      и...

      ✅ Получилось!!!

      ```diff\n+ {humanize(stealing)} ягод```
    """,  # noqa: E501
  ))
