import string

import crescent

from bot.command import cooldowns
from bot.command.plugin import _plugins
from bot.command.plugin.leader import _groups
from bot.utility import embeds

plugin = _plugins.Plugin()

period = cooldowns.Period(seconds=25)

name = "бананы"
description = "Бананы"


# Add a command to this command group.
@_groups.group.child
@plugin.include
# Register a hook to a command.
@crescent.hook(cooldowns.cooldown(1, period=period))
# Register a slash command.
@crescent.command(name=name, description=description)
class Bananas:
    # noinspection PyMethodMayBeStatic
    async def callback(self, context: crescent.Context) -> None:
        users = await plugin.model.database.bananas()

        title = "Бананы"

        description = string.whitespace

        # Return an enumerate object.
        for index, user in enumerate(users):
            position = index + 1

            description += f"*{position}*. <@{user.id}> Бананы: `{user.banana}`\n"

        embed = embeds.embed("default", title=title, description=description)

        # Respond to an interaction.
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
