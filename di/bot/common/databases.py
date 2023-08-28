import typing

import prisma as _prisma


class Database:
  def __init__(
    self: typing.Self,
    prisma: _prisma.Prisma,
  ) -> None:
    self.prisma = prisma

  async def connect(self: typing.Self) -> None:
    return await self.prisma.connect()

  async def disconnect(self: typing.Self) -> None:
    return await self.prisma.disconnect()

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
    banana: typing.Union[_prisma.types.AtomicIntInput, int],
    monkey: typing.Union[_prisma.types.AtomicIntInput, int],
    reputation: typing.Union[_prisma.types.AtomicIntInput, int],
    item: typing.Union[_prisma.types.AtomicIntInput, int]
  ) -> typing.Optional[_prisma.models.User]:
    return await self.prisma.user.update(
      _prisma.types.UserUpdateInput(
        banana=banana,
        monkey=monkey,
        reputation=reputation,
        item=item,
      ),
      where=_prisma.types.UserWhereUniqueInput(id=id__),
    )
