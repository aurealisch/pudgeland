import dataclasses
import typing

import prisma as _prisma

from . import typevars


@dataclasses.dataclass
class Effect:
  berry: typevars.Velocity
  fox: typevars.Velocity


Debuff = Effect
Buff = Effect


@dataclasses.dataclass
class Event:
  title: typing.Optional[str] = None
  description: typing.Optional[str] = None

  debuff: typing.Optional[Debuff] = None
  buff: typing.Optional[Buff] = None


@dataclasses.dataclass
class Configuration:
  events: typing.Optional[typing.Sequence[Event]]


class Berry:
  def __init__(
    self: typing.Self,
    configuration: Configuration,
    partial: _prisma.models.User,
  ) -> None:
    self.configuration = configuration
    self.partial = partial

  async def add(
    self: typing.Self,
    value: int,
  ) -> None:
    await self.partial.prisma().update(
      _prisma.types.UserUpdateInput(
        berry=self.partial.berry + value,
        fox=self.partial.fox,
        reputation=self.partial.reputation,
        item=self.partial.item,
      ),
      where=_prisma.types.UserWhereUniqueInput(id=self.partial.id),
    )
  
  async def remove(
    self: typing.Self,
    value: int,
  ) -> None:
    await self.partial.prisma().update(
      _prisma.types.UserUpdateInput(
        berry=self.partial.berry - value,
        fox=self.partial.fox,
        reputation=self.partial.reputation,
        item=self.partial.item,
      ),
      where=_prisma.types.UserWhereUniqueInput(id=self.partial.id),
    )


class Fox:
  def __init__(
    self: typing.Self,
    configuration: Configuration,
    partial: _prisma.models.User,
  ) -> None:
    self.configuration = configuration
    self.partial = partial

  async def add(
    self: typing.Self,
    value: int,
  ) -> None:
    await self.partial.prisma().update(
      _prisma.types.UserUpdateInput(
        berry=self.partial.berry,
        fox=self.partial.fox + value,
        reputation=self.partial.reputation,
        item=self.partial.item,
      ),
      where=_prisma.types.UserWhereUniqueInput(id=self.partial.id),
    )
  
  async def remove(
    self: typing.Self,
    value: int,
  ) -> None:
    await self.partial.prisma().update(
      _prisma.types.UserUpdateInput(
        berry=self.partial.berry,
        fox=self.partial.fox - value,
        reputation=self.partial.reputation,
        item=self.partial.item,
      ),
      where=_prisma.types.UserWhereUniqueInput(id=self.partial.id),
    )


class Reputation:
  def __init__(
    self: typing.Self,
    configuration: Configuration,
    partial: _prisma.models.User,
  ) -> None:
    self.configuration = configuration
    self.partial = partial

  async def add(
    self: typing.Self,
    value: int,
  ) -> None:
    await self.partial.prisma().update(
      _prisma.types.UserUpdateInput(
        berry=self.partial.berry,
        fox=self.partial.fox,
        reputation=self.partial.reputation + value,
        item=self.partial.item,
      ),
      where=_prisma.types.UserWhereUniqueInput(id=self.partial.id),
    )
  
  async def remove(
    self: typing.Self,
    value: int,
  ) -> None:
    await self.partial.prisma().update(
      _prisma.types.UserUpdateInput(
        berry=self.partial.berry,
        fox=self.partial.fox,
        reputation=self.partial.reputation - value,
        item=self.partial.item,
      ),
      where=_prisma.types.UserWhereUniqueInput(id=self.partial.id),
    )


class User:
  def __init__(
    self: typing.Self,
    configuration: Configuration,
    partial: _prisma.models.User,
  ) -> None:
    self.configuration = configuration
    self.partial = partial

    self.berry = Berry(
      configuration=self.configuration,
      partial=self.partial,
    )
    self.fox = Fox(
      configuration=self.configuration,
      partial=self.partial,
    )

    self.reputation = Reputation(
      configuration=self.configuration,
      partial=self.partial,
    )


class Economics:
  def __init__(
    self: typing.Self,
    configuration: Configuration,
    prisma: _prisma.Prisma,
  ) -> None:
    self.configuration = configuration
    self.prisma = prisma

  async def find_first_or_create(self: typing.Self, id: str) -> User:
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

    return User(self.configuration, partial=partial)

  async def find_many(
    self: typing.Self,
    take: int,
    user_keys: _prisma.types.UserKeys,
    sort_order: _prisma.types.SortOrder,
  ) -> typing.List[User]:
    order = {
      user_keys: sort_order
    }

    partials = await self.prisma.user.find_many(
      take,
      order=order,
    )

    users = map(
      lambda partial: User(
        self.configuration,
        partial=partial,
      ),
      partials,
    )

    return users
