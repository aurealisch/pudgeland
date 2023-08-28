import typing

import crescent
import hikari
import miru

from di.bot.common import shops
from di.bot.common.abc import commands, views
from di.bot.common.command import cooldowns, errors, utilities
from di.bot.common.type.alias.plugin import plugins
from di.bot.common.utility.embed import embeds

from . import _groups

plugin = plugins.Plugin()

period = cooldowns.Period(seconds=2.5)

_humanize = utilities.humanize


@_groups.group.child
@plugin.include
@crescent.hook(
  cooldowns.cooldown(
    1,
    period=period
  )
)
@crescent.command(name='покупка')
class PurchaseCommand(commands.CommandABC):
  async def run(
    self: typing.Self,
    context: crescent.Context,
  ) -> None:
    class View(views.ViewABC):
      @miru.text_select(
        options=[
          hikari.SelectMenuOption(
            label=item.label,
            value=value,
            description=item.description,
            emoji=item.emoji,
            is_default=False,
          )
          for value, item in shops.shop.items()
        ],
        placeholder='Предметы',
      )
      async def _(
        self: typing.Self,
        text_select: miru.TextSelect,
        context: miru.ViewContext,
      ) -> None:
        await context.defer()

        _item = int(text_select.values[0])

        item = shops.shop.get(_item)

        price = item.price

        _contextual = str(context.user.id)

        contextual = await plugin.model.database.find_first(_contextual)

        banana = contextual.banana

        if banana < price:
          raise errors.NotEnoughBananaError

        await plugin.model.database.update(
          _contextual,
          banana=banana - price,
          monkey=contextual.monkey,
          reputation=contextual.reputation,
          item=_item,
        )

        await context.respond(
          embed=embeds.embed(
            'default',
            context=context,
            description=f"""\
              <@{_contextual}> купил `{item.label}` за 🍌 `{_humanize(price)}` бананов
            """,
          )
        )

    view = View()

    components = view

    message = await context.respond(
      ensure_message=True,
      ephemeral=True,
      components=components,
      embed=embeds.embed(
        'default',
        context=context,
        description='✨ Выберите предмет для покупки',
      ),
    )

    if message is not None:
      await view.start(message)
