import random

import crescent
import hikari
import miru

from bot.common.plugin import plugins
from bot.common.command import commands, cooldowns, embeds
from bot.common.command.error import errors
from bot.common.command.view import views

plugin = plugins.Plugin()

period = cooldowns.Period(seconds=2.5)


@plugin.include
@crescent.hook(cooldowns.cooldown(1, period=period))
@crescent.command(name="приручать", description="Приручать")
class Command(commands.Command):
    async def run(self, context: crescent.Context) -> None:
        tame = plugin.model.configuration.plugins.tame

        _contextual = str(context.user.id)

        contextual = await plugin.model.database.find_first(_contextual)

        banana = contextual.banana
        monkey = contextual.monkey

        fed = (monkey + 1) * tame.price

        class View(views.View):
            @miru.button(label="ОК", style=hikari.ButtonStyle.SECONDARY, emoji="✅")
            async def ok(self, _: miru.Button, context: miru.ViewContext) -> None:
                if banana < fed:
                    raise errors.YouCantDoThatError

                banana -= fed

                if random.randint(1, tame.edge) != 1:
                    await plugin.model.database.update(
                        _contextual,
                        banana=banana,
                        monkey=monkey,
                        reputation=contextual.reputation,
                        item=contextual.item,
                    )

                    description = f"""\
                        <@{_contextual}> скормил 🍌 `{fed}` бананов
                        и...

                        ❌ Не получилось приручить обезьяну...
                    """

                    embed = embeds.embed(
                        "default",
                        context=context,
                        description=description,
                    )

                    await context.respond(embed=embed)

                    self.stop()

                await plugin.model.database.update(
                    _contextual,
                    banana=banana,
                    monkey=monkey + 1,
                    reputation=contextual.reputation,
                    item=contextual.item,
                )

                description = f"""\
                    <@{_contextual}> скормил 🍌 `{fed}` бананов
                    и...

                    ✅ Получилось приручить обезьяну!!!
                """

                embed = embeds.embed(
                    "default",
                    context=context,
                    description=description,
                )

                await context.respond(embed=embed)

                self.stop()

            @miru.button(
                label="Отменить", style=hikari.ButtonStyle.SECONDARY, emoji="❌"
            )
            async def cancel(self, _: miru.Button, context: miru.ViewContext) -> None:
                description = "Отменено"

                embed = embeds.embed(
                    "default",
                    context=context,
                    description=description,
                )

                await context.respond(embed=embed)

                self.stop()

        view = View()

        components = view

        description = (
            f"Чтобы попробовать приручить обезьяну, потребуется скормить 🍌 `{fed}`"
        )

        embed = embeds.embed("default", context=context, description=description)

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
