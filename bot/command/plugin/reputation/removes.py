import crescent
import hikari

from bot.command.cooldown import cooldowns
from bot.command.error import errors
from bot.command.plugin import _plugins
from bot.command.plugin.reputation import _groups
from bot.utility import embeds

plugin = _plugins.Plugin()

period = cooldowns.Period(hours=6)


# Add a command to this command group.
@_groups.group.child
@plugin.include
# Register a hook to a command.
@crescent.hook(cooldowns.cooldown(1, period=period))
# Register a slash command.
@crescent.command(name="убрать", description="Убрать")
class Remove:
    # An option when declaring a command using class syntax.
    user = crescent.option(hikari.User, name="пользователь", description="Пользователь")

    # noinspection PyMethodMayBeStatic
    async def callback(self, context: crescent.Context) -> None:
        # Defer this interaction response,
        # allowing you to respond within the next 15 minutes.
        await context.defer()

        # Create a new string object from the given object.
        _selfish = str(self.user.id)
        _contextish = str(context.user.id)

        if _selfish == _contextish:
            raise errors.YouCantDoThat

        selfish = await plugin.model.database.find_first(_selfish)

        banana = selfish.banana
        monkey = selfish.monkey
        reputation = selfish.reputation
        item = selfish.item

        reputation -= 1

        selfish = await plugin.model.database.middleware.update(
            _selfish,
            banana=banana,
            monkey=monkey,
            reputation=reputation,
            item=item,
        )

        reputation = selfish.reputation

        title = "Убрать"
        description = f"""\
            <@{_contextish}> убрал репутацию <@{_selfish}>

            📉 Репутация: `{reputation}`
        """

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
