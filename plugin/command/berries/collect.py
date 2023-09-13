import random

from bot.common import plugins

from .constant.groups import group
from .constant.periods import period

plugin = plugins.Plugin()

commands = plugin.commands
contexts = plugin.contexts


@commands.command(
  plugin,
  name='собрать',
  description='Собрать ягоды',
  period=period,
  group=group,
)
async def callback(context: contexts.Context) -> None:
  _ = context.humanize

  _contextual = str(context.user.id)

  contextual = await plugin.model.economics.find_first_or_create(_contextual)

  fox = contextual.partial.fox

  _item = contextual.partial.item

  collect = plugin.model.configuration.plugins.collect
  events = plugin.model.economics.events

  total = 0

  berrying = random.choice(range(
    collect.berrying.a,
    collect.berrying.b,
  ))

  if events:
    for event in events:
      buff = event.buff

      if buff:
        _berry = buff.berry

        berrying *= _berry

  if _item:
    item = plugin.model.economics.shop.get(_item)

    bonus = item.bonus

    if bonus.berry:
      berrying += round(berrying * bonus.berry)

  berrying = round(berrying)

  total += berrying

  description = f'Вы собрали {context.emoji.berry} `{_(berrying)}` ягод'

  if fox:
    foxying = fox * random.choice(range(
      collect.foxying.a,
      collect.foxying.b,
    ))

    if events:
      for event in events:
        buff = event.buff

        if buff:
          _fox = buff.fox

          foxying *= _fox

    if _item:
      item = plugin.model.economics.shop.get(_item)

      bonus = item.bonus

      if bonus.fox:
        foxying += round(foxying * bonus.fox)

    foxying = round(foxying)

    total += foxying

    description += f'\n+ {context.emoji.berry} `{_(foxying)}` ягод от {context.emoji.fox} `{_(fox)}` лис'  # noqa: E501
    description += f'\n\n🔁 Всего: {context.emoji.berry} `{_(total)}` ягод'

  await contextual.berry.add(total)

  await context.respond(embed=context.embed(
    'default',
    description=description,
  ))
