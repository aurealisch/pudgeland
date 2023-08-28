import typing

import crescent
import hikari
import miru

from di.bot.common.abc.command import commands
from di.bot.common.abc.view import views
from di.bot.common.command.cooldown.hook import cooldowns
from di.bot.common.command.error import errors
from di.bot.common.command.utility import utilities
from di.bot.common.shop import shops
from di.bot.common.type.alias.plugin import plugins
from di.bot.common.utility.embed import embeds

from . import _groups

plugin = plugins.Plugin()

period = cooldowns.PeriodDTO(seconds=2.5)

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
        emojis = plugin.model.configuration.emojis

        await context.defer()

        _item = int(text_select.values[0])

        item = shops.shop[_item]

        label = item.label
        price = item.price

        _contextual = str(context.user.id)

        contextual = await plugin.model.database.find_first(_contextual)

        x = contextual.x

        if x < price:
          raise errors.NotEnoughBananaError

        await plugin.model.database.update(
          _contextual,
          x=x - price,
          y=contextual.y,
          reputation=contextual.reputation,
          item=_item,
        )

        # fmt: off
        description = (
          f'<@{_contextual}> купил `{label}` за {emojis.x} `{_humanize(price)}`'
        )
        # fmt: on

        embed = embeds.embed(
          'default',
          context=context,
          description=description,
        )

        await context.respond(embed=embed)

    view = View()

    components = view

    description = '✨ Выберите предмет для покупки'

    embed = embeds.embed(
      'default',
      context=context,
      description=description,
    )

    message = await context.respond(
      ensure_message=True,
      ephemeral=True,
      components=components,
      embed=embed,
    )

    if message is not None:
      await view.start(message)
