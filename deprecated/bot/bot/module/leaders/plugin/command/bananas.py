import string

import crescent

from bot.common.command import commands, cooldowns, embeds, utilities
from bot.common.plugin import plugins
from bot.module.leaders.service import leaders

from . import _emojis, _groups, _periods

plugin = plugins.Plugin()

_ = utilities.humanize


@_groups.group.child
@plugin.include
@crescent.hook(cooldowns.cooldown(1, period=_periods.period))
@crescent.command(name="бананы", description="Бананы")
class Command(commands.Command):
    async def run(self, context: crescent.Context) -> None:
        users = await leaders.LeadersService.leaders("banana")

        description = string.whitespace

        for index, user in enumerate(users):
            position = index + 1

            id__ = user.id
            banana = user.banana

            if position in _emojis.emoji:
                description += _emojis.emoji[position]

            description += f"#{position}. <@{id__}> Бананы: `{_(banana)}`\n"

        embed = embeds.embed("default", context=context, description=description)

        await context.respond(embed=embed)
