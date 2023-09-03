import typing

import crescent
import hikari

from bot.common import contexts, plugins
from bot.common.abc import commands
from bot.common.command import cooldowns, exceptions

from . import _groups, _periods

plugin = plugins.Plugin()


@typing.final
@_groups.group.child
@plugin.include
@crescent.hook(cooldowns.cooldown(period=_periods.period))
@crescent.command(name="понизить", description="Понизить репутацию пользователю")
class DowngradeCommand(commands.CommandABC):
    user = crescent.option(
        hikari.User,
        name="пользователь",
        description="Пользователь",
    )

    async def run(self, context: contexts.Context) -> None:
        await context.defer()

        contextual = str(context.user.id)
        optional = str(self.user.id)

        if contextual != optional:
            user = await plugin.model.economics.find_first_or_create(optional)

            await user.reputation.remove(1)

            await context.respond(
                embed=context.embed(
                    "default",
                    description=f"📉 <@{contextual}> понизил репутацию <@{optional}>",
                ),
            )

            return

        raise exceptions.YouCantDoThatException
