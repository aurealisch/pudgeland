import crescent

from bot.command import cooldowns
from bot.command.plugin import _plugins
from bot.shop import shops
from bot.utility import embeds

plugin = _plugins.Plugin()

period = cooldowns.Period(seconds=5)


@plugin.include
# Register a hook to a command.
@crescent.hook(cooldowns.cooldown(1, period=period))
# Register a slash command.
@crescent.command(name="профиль", description="Профиль")
class Profile:
    # noinspection PyMethodMayBeStatic
    async def callback(self, context: crescent.Context) -> None:
        # Defer this interaction response,
        # allowing you to respond within the next 15 minutes.
        await context.defer()

        # Create a new string object from the given object.
        _contextish = str(context.user.id)

        contextish = await plugin.model.database.find_first(_contextish)

        title = "Профиль"
        description = f"""\
            🍌 Бананы: `{contextish.banana}`
            🐒 Обезьян: `{contextish.monkey}`

            📊 Репутация: `{contextish.reputation}`
        """

        if contextish.item:
            # Return the value for key if key is in the dictionary, else default.
            item = shops.shop.get(str(contextish.item))

            description += f"\n📦 Предмет: `{item.name}`"

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
