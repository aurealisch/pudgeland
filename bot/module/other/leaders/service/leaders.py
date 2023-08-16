import typing

import prisma as _prisma
from bot.common import commons

from .utility.constant import leaders as _leaders


class LeadersService:
  @staticmethod
  async def leaders(
    user_keys: _prisma.types.UserKeys,
  ) -> typing.List[_prisma.models.User]:
    return await commons.database.find_many(
      _leaders.TAKE,
      user_keys=user_keys,
      sort_order=_leaders.SORT_ORDER,
    )
