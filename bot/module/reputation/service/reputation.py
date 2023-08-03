import typing

import prisma as _prisma
from bot.common import commons


@typing.final
class ReputationService:
    @staticmethod
    async def add(id__: typing.Union[str, _prisma.types.StringFilter]) -> None:
        user = await commons.database.find_first(id__)

        reputation = user.reputation

        reputation += 1

        await commons.database.update(
            id__,
            banana=user.banana,
            monkey=user.monkey,
            reputation=reputation,
            item=user.item,
        )

    @staticmethod
    async def remove(id__: typing.Union[str, _prisma.types.StringFilter]) -> None:
        user = await commons.database.find_first(id__)

        reputation = user.reputation

        reputation -= 1

        await commons.database.update(
            id__,
            banana=user.banana,
            monkey=user.monkey,
            reputation=reputation,
            item=user.item,
        )


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
