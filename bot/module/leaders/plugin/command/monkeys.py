import string

import crescent

from bot.common.command import commands, cooldowns, embeds, utilities
from bot.common.plugin import plugins
from bot.module.leaders.service import leaders

from . import _groups, _periods

plugin = plugins.Plugin()

_ = utilities.humanize


@_groups.group.child
@plugin.include
@crescent.hook(cooldowns.cooldown(1, period=_periods.period))
@crescent.command(name="обезьяны", description="Обезьяны")
class Command(commands.Command):
    async def run(self, context: crescent.Context) -> None:
        users = await leaders.LeadersService.leaders("monkey")

        description = string.whitespace

        for index, user in enumerate(users):
            position = index + 1

            id__ = user.id
            monkey = user.monkey

            description += f"*{position}*. <@{id__}> Обезьян: `{_(monkey)}`\n"

        embed = embeds.embed("default", context=context, description=description)

        await context.respond(embed=embed)
