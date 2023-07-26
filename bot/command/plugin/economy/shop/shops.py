import string

import crescent
import hikari

from bot.command import _plugins
from bot.command.economy.shop import _shops
from bot.command.middleware import middlewares

plugin = _plugins.Plugin()

name = "магазин"
description = "Магазин"


class Middleware(middlewares.Middleware):
    async def callback(self, context: crescent.Context) -> None:
        # Return a capitalized version of the string.
        title = name.capitalize()

        description = string.whitespace

        for id__, item in _shops.shop.items():
            description += f"""
                # {id__}. {item.name}

                Цена: 🍌 `{item.price}` бананов

                Описание:\n> {item.description}
            """

        embed = hikari.Embed(title=title, description=description)

        # Respond to an interaction.
        await context.respond(embed=embed)


@plugin.include
# Register a slash command.
@crescent.command(name=name, description=description)
class Shop:
    # noinspection PyMethodMayBeStatic
    async def callback(self, context: crescent.Context) -> None:
        return await Middleware(plugin).callback(context)


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
