import typing

import hikari
import miru

from trevigiano.client import plugins

from .common import groups, periods

plugin = plugins.Plugin()

views = plugin.views
commands = plugin.commands
contexts = plugin.contexts


@commands.command(
  plugin,
  name='купить',
  description='купить',
  period=periods.period,
  group=groups.group,
)
async def callback(context: 'contexts.Context') -> None:
  database = plugin.model.database
  store = database.store

  emojis = context.emojis
  embeds = context.embeds
  humanizes = context.humanizes

  emoji = emojis.Emoji
  embed = embeds.embed
  humanize = humanizes.humanize

  async def text_select(
    self: typing.Self,
    _text_select: 'miru.TextSelect',
    _context: 'miru.Context',
  ) -> None:
    await _context.defer()

    _item, *_ = _text_select.values

    item = store.get(int(_item))

    _contextual = str(_context.user.id)

    contextual = await database.find(_contextual)

    if contextual.partial.item != int(_item):
      berry = contextual.partial.berry

      price = item.price

      if berry < price:
        raise plugin.exceptions.NotEnoughBerriesException

      await contextual.berry.remove(price)

      await _context.respond(embed=embed(
        'default',
        description=f"""\
          Вы купили `{item.label}` за {emoji.berry} `{humanize(price)}` ягод
        """,  # noqa: E501
      ))

      return

    raise plugin.exceptions.YouCantDoThatException

  __name = 'View'
  __bases = (views.ViewABC,)
  __dict = {
    'text_select': miru.text_select(
      options=[
        hikari.SelectMenuOption(
          label=item.label,
          value=value,
          description=item.description,
          emoji=item.emoji,
          is_default=False,
        )
        for value, item in store
      ],
      placeholder='Предметы',
    )(text_select),
  }

  type__ = type(
    __name,
    __bases,
    __dict,
  )()

  components = type__

  message = await context.respond(
    ephemeral=True,
    components=components,
    embed=embed(
      'default',
      description='✨ Выберите предмет для покупки',
    ),
  )

  if not message:
    await components.start(message)
