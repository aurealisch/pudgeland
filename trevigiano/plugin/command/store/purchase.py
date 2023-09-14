import hikari
import miru

from bot.common import plugins

from .constant.groups import group
from .constant.periods import period

plugin = plugins.Plugin()

views = plugin.views
commands = plugin.commands
contexts = plugin.contexts


@commands.command(
  plugin,
  name='покупка',
  description='Покупка',
  period=period,
  group=group,
)
async def callback(context: contexts.Context) -> None:
  shop = plugin.model.economics.shop

  async def text_select(
    self: views.ViewABC,
    text_select: 'miru.TextSelect',
    view_context: 'miru.ViewContext',
  ) -> None:
    humanize = context.humanize

    await view_context.defer()

    _item, *_ = text_select.values

    item = plugin.model.economics.shop.get(int(_item))

    _contextual = str(view_context.user.id)

    contextual = await plugin.model.economics.find_first_or_create(_contextual)

    if contextual.partial.item != int(_item):
      berry = contextual.partial.berry

      price = item.price

      if berry < price:
        raise plugin.exceptions.NotEnoughBerriesException

      await contextual.berry.remove(price)

      await view_context.respond(embed=context.embed(
        'default',
        description=f"""\
          Вы купили `{item.label}` за {context.emoji.berry} `{humanize(price)}` ягод
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
        for value, item in shop
      ],
      placeholder='Предметы',
    )(text_select),
  }

  view = type(
    __name,
    __bases,
    __dict,
  )()

  components = view

  message = await context.respond(
    True,
    components=components,
    embed=context.embed(
      'default',
      description='✨ Выберите предмет для покупки',
    ),
    ensure_message=True,
  )

  if message is not None:
    await view.start(message)
