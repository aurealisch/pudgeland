import crescent
import hikari

from bot.plugin._cooldown import _cooldowns
from bot.plugin import _plugins
from bot.plugin._exception import _exceptions
from bot.plugin._middleware import _middlewares
from bot.plugin.reputation import _groups

plugin = _plugins.Plugin()

period = _cooldowns.Period(hours=6)

name = "убрать"
description = "Убрать"


class Middleware(_middlewares.Middleware):
    async def callback(self, context: crescent.Context) -> None:
        # Defer this interaction response,
        # allowing you to respond within the next 15 minutes.
        await context.defer(ephemeral=False)

        _optional = str(self.options.get("user").id)
        _contextual = str(context.user.id)

        if _optional == _contextual:
            raise _exceptions.YouCantDoThat

        optional = await plugin.model.database.find_first(_optional)

        await plugin.model.database.middleware.update(
            _optional,
            banana=optional.banana,
            monkey=optional.monkey,
            reputation=optional.reputation - 1,
            item=optional.item,
        )

        # Return a capitalized version of the string.
        title = name.capitalize()
        description = f"""\
            <@{_contextual}> убрал репутацию <@{_optional}>

            📉 Репутация: `{optional.reputation - 1}`
        """

        embed = hikari.Embed(title=title, description=description)

        # Respond to an interaction.
        await context.respond(embed=embed)


# Add a command to this command group.
@_groups.group.child
@plugin.include
# Register a hook to a command.
@crescent.hook(_cooldowns.cooldown(1, period=period))
# Register a slash command.
@crescent.command(name=name, description=description)
class Remove:
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
