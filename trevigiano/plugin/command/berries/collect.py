import random

from trevigiano.client import plugins

from .common import groups, periods

plugin = plugins.Plugin()

commands = plugin.commands
contexts = plugin.contexts


@commands.command(
  plugin,
  name='собрать',
  description='Собрать',
  period=periods.period,
  group=groups.group,
)
async def callback(context: 'contexts.Context') -> None:
  emojis = context.emojis
  embeds = context.embeds
  humanizes = context.humanizes

  emoji = emojis.Emoji
  embed = embeds.embed
  humanize = humanizes.humanize

  _contextual = str(context.user.id)

  contextual = await plugin.model.database.find(_contextual)

  fox = contextual.partial.fox

  _item = contextual.partial.item

  collect = plugin.model.configuration.plugins.collect
  events = plugin.model.database.events

  total = 0

  berrying = random.choice(range(
    collect.berry.start,
    collect.berry.stop,
  ))

  if events:
    for event in events:
      buff = event.buff

      if buff:
        _berry = buff.berry

        berrying *= _berry

  if _item:
    item = plugin.model.database.shop.get(_item)

    bonus = item.bonus

    if bonus.berry:
      berrying += round(berrying * bonus.berry)

  berrying = round(berrying)

  total += berrying

  description = f'Вы собрали {emoji.berry} `{humanize(berrying)}` ягод'

  if fox:
    foxying = fox * random.choice(range(
      collect.fox.start,
      collect.fox.stop,
    ))

    if events:
      for event in events:
        buff = event.buff

        if buff:
          _fox = buff.fox

          foxying *= _fox

    if _item:
      item = plugin.model.database.shop.get(_item)

      bonus = item.bonus

      if bonus.fox:
        foxying += round(foxying * bonus.fox)

    foxying = round(foxying)

    total += foxying

    description += f'\n+ {emoji.berry} `{humanize(foxying)}` ягод от {emoji.fox} `{humanize(fox)}` лис'  # noqa: E501
    description += f'\n\n🔁 Всего: {emoji.berry} `{humanize(total)}` ягод'

  await contextual.berry.add(total)

  await context.respond(embed=embed(
    'default',
    description=description,
  ))
