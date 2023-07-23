import typing

import attrs

import prisma as _prisma
from bot.common.database.middleware import middlewares


@attrs.define
class Database:
    middleware: middlewares.Middleware

    # noinspection PyMethodMayBeStatic
    async def find_first(
        self, id__: str | _prisma.types.StringFilter
    ) -> _prisma.models.User:
        user = await self.middleware.find_first(id__)

        if user is None:
            return await self.middleware.create(id__)

        return user

    # noinspection PyMethodMayBeStatic
    async def bananas(self) -> typing.List[_prisma.models.User]:
        return await self.middleware.find_many(
            5,
            user_keys="banana",
            sort_order="desc",
        )

    # noinspection PyMethodMayBeStatic
    async def monkeys(self) -> typing.List[_prisma.models.User]:
        return await self.middleware.find_many(
            5,
            user_keys="monkey",
            sort_order="desc",
        )

    # noinspection PyMethodMayBeStatic
    async def reputations(self) -> typing.List[_prisma.models.User]:
        return await self.middleware.find_many(
            5,
            user_keys="reputation",
            sort_order="desc",
        )


# MIT License
#
# Copyright (c) 2023 pudgeland
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
