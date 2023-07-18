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

import typing

__all__: typing.Sequence[str] = ("UserManager",)

import prisma as _prisma


class UserManager:
    def __init__(self, prisma: _prisma.Prisma) -> None:
        self.prisma = prisma

    async def find_first(
        self, *, id: str | _prisma.types.StringFilter = ...
    ) -> _prisma.models.User | None:
        """
        Other parameters
        -----------------
        `id` : `str` | `prisma.types.StringFilter`

        Returns
        -------
        `prisma.models.User` | `None`
        """
        user = await _prisma.models.User.prisma().find_first(
            where=_prisma.types.UserWhereInput(id=id)
        )

        if user is None:
            user = await _prisma.models.User.prisma().create(
                _prisma.types.UserCreateInput(id=id)
            )

        return user

    async def update(
        self,
        *,
        id: str = ...,
        banana: _prisma.types.AtomicIntInput | int = ...,
        monkey: _prisma.types.AtomicIntInput | int = ...,
    ) -> _prisma.models.User | None:
        """
        Other parameters
        ----------------
        - `id` : `str`
        - `banana` : `types.AtomicIntInput` | `int`
        - `monkey` : `types.AtomicIntInput` | `int`

        Returns
        -------
        `prisma.models.User` | `None`
        """
        return await _prisma.models.User.prisma().update(
            _prisma.types.UserUpdateInput(
                banana=banana,
                monkey=monkey,
            ),
            where=_prisma.types.UserWhereUniqueInput(id=id),
        )
