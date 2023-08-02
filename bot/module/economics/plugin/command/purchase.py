import crescent
import hikari
import miru

from bot.common.command import commands
from bot.common.command.cooldown import cooldowns
from bot.common.command.embed import embeds
from bot.common.command.error import errors
from bot.common.command.view import views
from bot.common.plugin import plugins
from bot.module.economics.shop import shops

plugin = plugins.Plugin()

period = cooldowns.Period(seconds=2.5)

name = "покупка"
description = "Покупка"


@plugin.include
@crescent.hook(cooldowns.cooldown(1, period=period))
@crescent.command(name=name, description=description)
class Command(commands.Command):
    async def run(self, context: crescent.Context) -> None:
        class View(views.View):
            @miru.text_select(
                options=[
                    hikari.SelectMenuOption(
                        label=item.label,
                        value=value,
                        description=item.description,
                        emoji=item.emoji,
                        is_default=False,
                    )
                    for value, item in shops.shop.items()
                ]
            )
            async def _(
                self, text_select: miru.TextSelect, _context: miru.ViewContext
            ) -> None:
                _item = text_select.values[0]

                item = shops.shop[_item]

                label = item.label
                price = item.price

                _contextual = str(_context.user.id)

                contextual = await plugin.model.database.find_first(_contextual)

                banana = contextual.banana

                if banana < price:
                    raise errors.NotEnoughBananaError

                await plugin.model.database.middleware.update(
                    _contextual,
                    banana=banana,
                    monkey=contextual.monkey,
                    reputation=contextual.reputation,
                    item=int(_item),
                )

                # fmt: off
                _description = (
                    f"<@{_contextual}> купил `{label}` за 🍌 `{price}` бананов"
                )
                # fmt: on

                _embed = embeds.embed(
                    "default", context=_context, description=_description
                )

                await _context.respond(embed=_embed)

        view = View()

        components = view

        _description = "✨ Выберите предмет для покупки"

        embed = embeds.embed("default", context=context, description=_description)

        message = await context.respond(
            ensure_message=True,
            ephemeral=True,
            components=components,
            embed=embed,
        )

        if message is not None:
            await view.start(message)


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
