import typing

import attrs

import prisma as _prisma


@attrs.define
class Database:
  prisma: _prisma.Prisma

  async def find_first(
    self, id__: typing.Union[str, _prisma.types.StringFilter]
  ) -> typing.Optional[_prisma.models.User]:
    user = await self.prisma.user.find_first(
      where=_prisma.types.UserWhereInput(id=id__)
    )

    if user is None:
      return await self.create(id__)

    return user

  async def find_many(
    self,
    take: int,
    user_keys: _prisma.types.UserKeys,
    sort_order: _prisma.types.SortOrder,
  ) -> typing.List[_prisma.models.User]:
    order = {user_keys: sort_order}

    return await self.prisma.user.find_many(take, order=order)

  async def create(self, id__: str) -> _prisma.models.User:
    return await self.prisma.user.create(_prisma.types.UserCreateInput(id=id__))

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
        banana=banana,
        monkey=monkey,
        reputation=reputation,
        item=item,
      ),
      where=_prisma.types.UserWhereUniqueInput(id=id__),
    )
