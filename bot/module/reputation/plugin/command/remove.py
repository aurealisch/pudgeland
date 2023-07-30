import crescent

from bot.common.command import commands
from bot.common.command.cooldown import cooldowns
from bot.common.plugin import plugins
from bot.module.reputation.plugin.command import _group, _period

plugin = plugins.Plugin()

name = "убрать"
description = "Убрать репутацию пользователю"


# Add a command to this command group.
@_group.group.child
@plugin.include
# Register a hook to a command.
@crescent.hook(cooldowns.cooldown(1, period=_period.period))
#  Register a slash command
@crescent.command(name=name, description=description)
class Command(commands.Command):
    async def callback(self, context: crescent.Context) -> None:
        pass


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
