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
from __future__ import annotations

__all__: typing.Sequence[str] = ("Middleware",)

import random
import typing

import crescent
import hikari

from bot.common.environment import environments
from bot.plugin.middleware import middlewares


class Middleware(middlewares.Middleware):
    async def callback(self, context: crescent.Context) -> None:
        """
        Parameters
        ----------
        - `context` : `crescent.Context`
        """
        id = str(context.user.id)

        user = await self.plugin.model.database.users.find_first(id=id)

        banana = user.banana
        monkey = user.monkey

        collecting = random.choice(
            range(
                environments.by_hand_minimal,
                environments.by_hand_maximum,
            )
        )

        await self.plugin.model.database.users.update(
            id=id,
            banana=banana + collecting,
            monkey=monkey,
        )

        await context.respond(
            embed=hikari.Embed(
                title="Собирать",
                description=f"""
                    <@{id}> собрал `{collecting}` бананов

                    :banana: Бананы: `{banana + collecting}`
                    :monkey: Обезьяны: `{monkey}`
                """,
            )
        )
