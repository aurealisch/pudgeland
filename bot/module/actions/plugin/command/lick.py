import crescent
import hikari

from bot.common.plugin import plugins
from bot.common.command import commands, cooldowns, embeds
from bot.common.command.error import errors
from bot.module.actions.service.api.client import clients
from bot.module.actions.service.api.types import categories

from . import _periods

plugin = plugins.Plugin()


@plugin.include
@crescent.hook(cooldowns.cooldown(1, period=_periods.period))
@crescent.command(name="лизнуть", description="Лизнуть пользователя")
class Command(commands.Command):
    user = crescent.option(hikari.User, name="пользователь", description="Пользователь")

    async def run(self, context: crescent.Context) -> None:
        await context.defer()

        contextual = str(context.user.id)
        optional = str(self.user.id)

        if contextual.__eq__(optional):
            raise errors.YouCantDoThatError

        description = f"<@{contextual}> лижет <@{optional}>"

        url = clients.Client().sfw.search(categories.SfwCategory.LICK).url

        image = url

        embed = embeds.embed(
            "default",
            context=context,
            description=description,
            image=image,
        )

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
