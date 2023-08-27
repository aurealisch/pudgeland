import typing

import attrs

import prisma as _prisma


@attrs.define
class Database:
  prisma: _prisma.Prisma

  async def find_first(
    self: typing.Self,
    id__: typing.Union[str, _prisma.types.StringFilter]
  ) -> typing.Optional[_prisma.models.User]:
    user = await self.prisma.user.find_first(
      where=_prisma.types.UserWhereInput(id=id__)
    )

    if user is None:
      return await self.create(id__)

    return user

  async def find_many(
    self: typing.Self,
    take: int,
    user_keys: _prisma.types.UserKeys,
    sort_order: _prisma.types.SortOrder,
  ) -> typing.List[_prisma.models.User]:
    order = {user_keys: sort_order}

    return await self.prisma.user.find_many(take, order=order)

  async def create(
    self: typing.Self,
    id__: str,
  ) -> _prisma.models.User:
    return await self.prisma.user.create(_prisma.types.UserCreateInput(id=id__))

  async def update(
    self: typing.Self,
    id__: str,
    *,
    x: typing.Union[_prisma.types.AtomicIntInput, int],
    y: typing.Union[_prisma.types.AtomicIntInput, int],
    reputation: typing.Union[_prisma.types.AtomicIntInput, int],
    item: typing.Union[_prisma.types.AtomicIntInput, int]
  ) -> typing.Optional[_prisma.models.User]:
    return await self.prisma.user.update(
      _prisma.types.UserUpdateInput(
        x=x,
        y=y,
        reputation=reputation,
        item=item,
      ),
      where=_prisma.types.UserWhereUniqueInput(id=id__),
    )
