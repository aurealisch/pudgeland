import typing

import prisma as _prisma
from trevigiano import shop


class Resource:
    def __init__(
        self: typing.Self,
        key: typing.Literal[
            "berry",
            "fox",
            "reputation",
        ],
        partial: "_prisma.models.User",
    ) -> None:
        self.key = key
        self.partial = partial

    async def add(self: typing.Self, value: int) -> None:
        await self.partial.prisma().update(
            {self.key: self.partial.dict().get(self.key) + value},
            where=_prisma.types.UserWhereUniqueInput(id=self.partial.id),
        )

    async def remove(self: typing.Self, value: int) -> None:
        await self.partial.prisma().update(
            {self.key: self.partial.dict().get(self.key) - value},
            where=_prisma.types.UserWhereUniqueInput(id=self.partial.id),
        )


class User:
    def __init__(self: typing.Self, partial: "_prisma.models.User") -> None:
        self.partial = partial

        self.berry = Resource("berry", partial=self.partial)
        self.fox = Resource("fox", partial=self.partial)

        self.reputation = Resource("reputation", partial=self.partial)


class Database:
    def __init__(self: typing.Self, prisma: "_prisma.Prisma") -> None:
        self.prisma = prisma
        self.shop = shop.shop

    async def find(self: typing.Self, id__: str) -> User:
        PARTIAL = await self.prisma.user.find_first(
            where=_prisma.types.UserWhereInput(id=id__)
        )

        if PARTIAL is None:
            PARTIAL = await self.prisma.user.create(
                _prisma.types.UserCreateInput(id=id)
            )

        return User(partial=PARTIAL)

    async def leaders(
        self: typing.Self,
        take: int,
        user_keys: "_prisma.types.UserKeys",
        sort_order: "_prisma.types.SortOrder",
    ) -> typing.List[User]:
        PARTIALS = await self.prisma.user.find_many(take, order={user_keys: sort_order})

        return map(lambda PARTIAL: User(partial=PARTIAL), PARTIALS)
