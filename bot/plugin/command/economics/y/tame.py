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
@crescent.command(name='приручать')
class Command(commands.Command):
  """."""

  async def run(self, context: crescent.Context) -> None:
    """."""
    tame = plugin.model.configuration.plugins.tame
    emojis = plugin.model.configuration.emojis

    _contextual = str(context.user.id)

    contextual = await plugin.model.database.find_first(_contextual)

    x = contextual.x

    fed = (x + 1) * tame.price

    class View(views.View):
      """."""

      @miru.button(label='ОК', style=hikari.ButtonStyle.SECONDARY, emoji='✅')
      async def ok(self, _: miru.Button, context: miru.ViewContext) -> None:
        """."""
        await context.defer()

        x = contextual.x

        if x < fed:
          raise errors.NotEnoughBananaError

        x -= fed

        if random.choice(
          range(
            1,
            tame.edge,
          )
         ) != 1:
          await plugin.model.database.update(
            _contextual,
            x=x,
            y=y,
            reputation=contextual.reputation,
            item=contextual.item,
          )

          description = f"""\
            <@{_contextual}> скормил {emojis.x} `{_humanize(fed)}`
            и...

            ❌ Не получилось приручить...
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
          x=x,
          y=y + 1,
          reputation=contextual.reputation,
          item=contextual.item,
        )

        description = f"""\
          <@{_contextual}> скормил {emojis.x} `{_humanize(fed)}`
          и...

          ✅ Получилось приручить!!!
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

        flags = hikari.MessageFlag.EPHEMERAL

        await context.respond(
          embed=embed,
          flags=flags,
        )

        self.stop()

    view = View()

    components = view

    description = (
      f'Чтобы попробовать приручить, потребуется скормить {emojis.x} `{_humanize(fed)}`'
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
