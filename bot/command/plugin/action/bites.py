import collei
import crescent
import hikari

from bot.command import _plugins
from bot.command.exception import exceptions
from bot.command.middleware import middlewares

plugin = _plugins.Plugin()

name = "укусить"
description = "Укусить пользователя"


class Middleware(middlewares.Middleware):
    async def callback(self, context: crescent.Context) -> None:
        optional = str(self.options.get("user").id)
        contextual = context.user.id

        if optional == contextual:
            raise exceptions.YouCantDoThat

        title = "Укусить"
        description = f"<@{contextual}> кусает <@{optional}>"

        embed = hikari.Embed(title=title, description=description)

        # Set the image on this embed.
        embed.set_image(collei.Client().sfw.get(collei.SfwCategory.BITE).url)

        # Respond to an interaction.
        await context.respond(embed=embed)


@plugin.include
# Register a slash command.
@crescent.command(name=name, description=description)
class Bite:
    # An option when declaring a command using class syntax.
    user = crescent.option(hikari.User, name="пользователь", description="Пользователь")

    # noinspection PyMethodMayBeStatic
    async def callback(self, context: crescent.Context) -> None:
        return await Middleware(plugin, options={"user": self.user}).callback(context)


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
