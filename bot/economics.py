import dataclasses
import typing

import prisma as _prisma

from . import types
from .common import shops


@typing.final
@dataclasses.dataclass
class Effect:
    berry: "types.FloatOrInt"
    fox: "types.FloatOrInt"


Debuff = Effect
Buff = Effect


@typing.final
@dataclasses.dataclass
class Event:
    title: typing.Optional[str] = None
    description: typing.Optional[str] = None
    debuff: typing.Optional[Debuff] = None
    buff: typing.Optional[Buff] = None


@typing.final
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

    async def add(
        self: typing.Self,
        value: int,
    ) -> None:
        await self.partial.prisma().update(
            {self.key: self.partial.dict().get(self.key) + value},
            where={"id": self.partial.id},
        )

    async def remove(
        self: typing.Self,
        value: int,
    ) -> None:
        await self.partial.prisma().update(
            {self.key: self.partial.dict().get(self.key) - value},
            where={"id": self.partial.id},
        )


@typing.final
class User:
    def __init__(
        self: typing.Self,
        partial: "_prisma.models.User",
    ) -> None:
        self.partial = partial

        self.berry = Resource("berry", partial=self.partial)
        self.fox = Resource("fox", partial=self.partial)

        self.reputation = Resource("reputation", partial=self.partial)


@typing.final
class Economics:
    def __init__(
        self: typing.Self,
        prisma: "_prisma.Prisma",
        events: typing.Optional[typing.Sequence[Event]] = None,
    ) -> None:
        self.prisma = prisma
        self.events = events
        self.shop = shops.shop

    async def find_first_or_create(
        self: typing.Self,
        id: str,
    ) -> User:
        partial = await self.prisma.user.find_first(
            where=_prisma.types.UserWhereInput(
                id=id,
            ),
        )

        if partial is None:
            partial = await self.prisma.user.create(
                _prisma.types.UserCreateInput(
                    id=id,
                ),
            )

        return User(partial=partial)

    async def find_many(
        self: typing.Self,
        take: int,
        user_keys: "_prisma.types.UserKeys",
        sort_order: "_prisma.types.SortOrder",
    ) -> typing.List[User]:
        order = {user_keys: sort_order}

        partials = await self.prisma.user.find_many(take, order=order)

        users = map(lambda partial: User(partial=partial), partials)

        return users
