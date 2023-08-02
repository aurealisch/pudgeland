import typing

import attrs

import prisma as _prisma


@typing.final
@attrs.define
class Database:
    prisma: _prisma.Prisma

    # noinspection PyMethodMayBeStatic
    async def find_first(
        self, id__: typing.Union[str, _prisma.types.StringFilter]
    ) -> typing.Optional[_prisma.models.User]:
        user = await self.prisma.user.find_first(
            where=_prisma.types.UserWhereInput(id=id__)
        )

        if user is None:
            return await self.middleware.create(id__)

        return user

    # noinspection PyMethodMayBeStatic
    async def find_many(
        self,
        take: int,
        user_keys: _prisma.types.UserKeys,
        sort_order: _prisma.types.SortOrder,
    ) -> typing.List[_prisma.models.User]:
        order = {user_keys: sort_order}

        return await self.prisma.user.find_many(take, order=order)

    # noinspection PyMethodMayBeStatic
    async def create(self, id__: str) -> _prisma.models.User:
        return await self.prisma.user.create(_prisma.types.UserCreateInput(id=id__))

    # noinspection PyMethodMayBeStatic
    async def update(
        self,
        id__: str,
        *,
        banana: typing.Union[_prisma.types.AtomicIntInput, int],
        monkey: typing.Union[_prisma.types.AtomicIntInput, int],
        reputation: typing.Union[_prisma.types.AtomicIntInput, int],
        item: typing.Union[_prisma.types.AtomicIntInput, int]
    ) -> typing.Optional[_prisma.models.User]:
        return await self.prisma.user.update(
            _prisma.types.UserUpdateInput(
                banana=banana, monkey=monkey, reputation=reputation, item=item
            ),
            where=_prisma.types.UserWhereUniqueInput(id=id__),
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
