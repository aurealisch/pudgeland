import typing

import crescent
import hikari
import miru

from bot.common import contexts, shops
from bot.common.abc import command_abc, view_abc
from bot.common.command import cooldowns, errors
from bot.common.type.alias.plugin import plugins

from . import _groups

plugin = plugins.Plugin()

period = cooldowns.Period(seconds=2, milliseconds=500)


@_groups.group.child
@plugin.include
@crescent.hook(cooldowns.cooldown(period=period))
@crescent.command(
  name='покупка',
  description='Покупка',
)
class PurchaseCommand(command_abc.CommandABC):
  async def run(
    self: typing.Self,
    context: contexts.Context,
  ) -> None:
    await context.defer(ephemeral=True)


    class View(view_abc.ViewABC):
      @miru.text_select(
        options=[
          hikari.SelectMenuOption(
            label=item.label,
            value=value,
            description=item.description,
            emoji=item.emoji,
            is_default=False,
          )
          for (
            value,
            item
          ) in shops.shop.items()
        ],
        placeholder='Предметы',
      )
      async def _(
        self: typing.Self,
        text_select: miru.TextSelect,
        view_context: miru.ViewContext,
      ) -> None:
        await view_context.defer()

        _item = int(text_select.values[0])

        item = shops.shop.get(_item)

        _contextual = str(view_context.user.id)

        contextual = await plugin.model.economics.find_first_or_create(_contextual)

        if contextual.partial.item != _item:
          berry = contextual.partial.berry

          price = item.price

          if berry < price:
            raise errors.NotEnoughBerriesError

          await contextual.berry.remove(price)

          await view_context.respond(embed=context.embed(
            'default',
            description=f"""\
              <@{_contextual}> купил `{item.label}` за {context.emoji.berry} `{context.humanize(price)}` ягод
            """,
          ))

          return

        raise errors.YouCantDoThatError


    view = View()

    components = view

    message = await context.respond(
      ensure_message=True,
      ephemeral=True,
      components=components,
      embed=context.embed(
        'default',
        description='✨ Выберите предмет для покупки',
      ),
    )

    if message is not None:
      await view.start(message)
