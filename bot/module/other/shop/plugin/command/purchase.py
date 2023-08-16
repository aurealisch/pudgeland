import crescent
import hikari
import miru

from bot.common.command import commands, cooldowns, embeds, utilities, views
from bot.common.command.error import errors
from bot.common.plugin import plugins
from bot.common.shop import shops

from . import _groups

plugin = plugins.Plugin()

period = cooldowns.Period(seconds=2.5)

_ = utilities.humanize


@_groups.group.child
@plugin.include
@crescent.hook(cooldowns.cooldown(1, period=period))
@crescent.command(
  name='покупка',
  description='Покупка',
)
class Command(commands.Command):
  async def run(self, context: crescent.Context) -> None:
    class View(views.View):
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
        self, text_select: miru.TextSelect, context: miru.ViewContext
      ) -> None:
        await context.defer()

        _item = text_select.values[0]

        item = shops.shop[_item]

        label = item.label
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
          item=int(_item),
        )

        # fmt: off
        description = (
          f'<@{_contextual}> купил `{label}` за 🍌 `{_(price)}` бананов'
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
