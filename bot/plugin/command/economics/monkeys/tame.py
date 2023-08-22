"""."""

import random

import crescent
import hikari
import miru

from bot.common.command import (
  commands,
  cooldowns,
  embeds,
  utilities,
  views
)
from bot.common.command.error import errors
from bot.common import plugins

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
@crescent.command(
  name='приручать',
  description='Приручать',
)
class Command(commands.Command):
  """."""

  async def run(self, context: crescent.Context) -> None:
    """."""
    tame = plugin.model.configuration.plugins.tame

    _contextual = str(context.user.id)

    contextual = await plugin.model.database.find_first(_contextual)

    monkey = contextual.monkey

    fed = (monkey + 1) * tame.price

    class View(views.View):
      """."""

      @miru.button(label='ОК', style=hikari.ButtonStyle.SECONDARY, emoji='✅')
      async def ok(self, _: miru.Button, context: miru.ViewContext) -> None:
        """."""
        await context.defer()

        banana = contextual.banana

        if banana < fed:
          raise errors.NotEnoughBananaError

        banana -= fed

        if random.choice(
          range(
            1,
            tame.edge,
          )
         ) != 1:
          await plugin.model.database.update(
            _contextual,
            banana=banana,
            monkey=monkey,
            reputation=contextual.reputation,
            item=contextual.item,
          )

          description = f"""\
            <@{_contextual}> скормил 🍌 `{_humanize(fed)}` бананов
            и...

            ❌ Не получилось приручить обезьяну...
          """

          embed = embeds.embed(
            'default',
            context=context,
            description=description,
          )

          await context.respond(embed=embed)

          self.stop()

          return

        await plugin.model.database.update(
          _contextual,
          banana=banana,
          monkey=monkey + 1,
          reputation=contextual.reputation,
          item=contextual.item,
        )

        description = f"""\
          <@{_contextual}> скормил 🍌 `{_humanize(fed)}` бананов
          и...

          ✅ Получилось приручить обезьяну!!!
        """

        embed = embeds.embed(
          'default',
          context=context,
          description=description,
        )

        await context.respond(embed=embed)

        self.stop()

      @miru.button(
        label='Отменить', style=hikari.ButtonStyle.SECONDARY, emoji='❌'
      )
      async def cancel(self, _: miru.Button, context: miru.ViewContext) -> None:
        """."""
        await context.defer()

        description = 'Отменено'

        embed = embeds.embed(
          'default',
          context=context,
          description=description,
        )

        await context.respond(embed=embed, flags=hikari.MessageFlag.EPHEMERAL)

        self.stop()

    view = View()

    components = view

    description = (
      f'Чтобы попробовать приручить обезьяну, потребуется скормить 🍌 `{_humanize(fed)}`'
    )

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
