import crescent

from bot.command.cooldown import cooldowns
from bot.command.middleware import middlewares
from bot.command.plugin import _plugins
from bot.command.plugin.economy.shop import _shops
from bot.utility import embeds

plugin = _plugins.Plugin()

period = cooldowns.Period(seconds=5)

name = "профиль"
description = "Профиль"


class Middleware(middlewares.Middleware):
    async def callback(self, context: crescent.Context) -> None:
        # Defer this interaction response,
        # allowing you to respond within the next 15 minutes.
        await context.defer(ephemeral=False)

        user = await self.plugin.model.database.find_first(str(context.user.id))

        # Return a capitalized version of the string.
        title = name.capitalize()
        description = f"""\
            🍌 Бананы: `{user.banana}`
            🐒 Обезьян: `{user.monkey}`

            📊 Репутация: `{user.reputation}`
        """

        if user.item:
            # Return the value for key if key is in the dictionary, else default.
            item = _shops.shop.get(str(user.item))

            description += f"\n📦 Предмет: `{item.name}`"

        embed = embeds.embed("default", title=title, description=description)

        # Respond to an interaction.
        await context.respond(embed=embed)


@plugin.include
# Register a hook to a command.
@crescent.hook(cooldowns.cooldown(1, period=period))
# Register a slash command.
@crescent.command(name=name, description=description)
class Profile:
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
