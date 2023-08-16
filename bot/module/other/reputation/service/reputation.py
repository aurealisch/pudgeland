import typing

import prisma as _prisma
from bot.common import commons


class ReputationService:
  @staticmethod
  async def upgrade(id__: typing.Union[str, _prisma.types.StringFilter]) -> None:
    user = await commons.database.find_first(id__)

    reputation = user.reputation

    reputation += 1

    await commons.database.update(
      id__,
      banana=user.banana,
      monkey=user.monkey,
      reputation=reputation,
      item=user.item,
    )

  @staticmethod
  async def downgrade(id__: typing.Union[str, _prisma.types.StringFilter]) -> None:
    user = await commons.database.find_first(id__)

    reputation = user.reputation

    reputation -= 1

    await commons.database.update(
      id__,
      banana=user.banana,
      monkey=user.monkey,
      reputation=reputation,
      item=user.item,
    )
