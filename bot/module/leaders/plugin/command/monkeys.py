import string

import crescent

from bot.common.command import commands
from bot.common.command.cooldown import cooldowns
from bot.common.command.embed import embeds
from bot.common.plugin import plugins
from bot.module.leaders.service import leaders

from . import _groups, _periods

plugin = plugins.Plugin()


@_groups.group.child
@plugin.include
@crescent.hook(cooldowns.cooldown(1, period=_periods.period))
@crescent.command(name="обезьяны", description="Обезьяны")
class Command(commands.Command):
    async def run(self, context: crescent.Context) -> None:
        await context.defer()

        users = await leaders.LeadersService.leaders("monkey")

        description = string.whitespace

        for index, user in enumerate(users):
            position = index + 1

            id__ = user.id
            monkey = user.monkey

            description += f"*{position}*. <@{id__}> Обезьян: `{monkey}`"

        embed = embeds.embed("default", context=context, description=description)

        await context.respond(embed=embed)


# MIT License
#
# Copyright (c) 2023 elaresai
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in all
# copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.
