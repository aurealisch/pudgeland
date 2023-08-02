import crescent
import yarl

from bot.common import plugins
from bot.common.command import commands, cooldowns, embeds
from bot.module.miscellaneous.service.api import clients

plugin = plugins.Plugin()

period = cooldowns.Period(seconds=2.5)


@plugin.include
@crescent.hook(cooldowns.cooldown(1, period=period))
@crescent.command(name="кошка", description="Случайное изображение кошки")
class Command(commands.Command):
    async def run(self, context: crescent.Context) -> None:
        _url = yarl.URL("https://api.thecatapi.com/v1/images/search")

        url = clients.Client(_url).image.search().url

        image = url

        embed = embeds.embed("default", context=context, image=image)

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
