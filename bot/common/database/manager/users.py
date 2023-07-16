import attrs

import prisma
from prisma import models, types


@attrs.define
class UserManager:
    prisma: prisma.Prisma

    async def find(self, *, id: str | types.StringFilter = ...) -> models.User | None:
        user = await models.User.prisma().find_first(where=types.UserWhereInput(id=id))

        if user is None:
            user = await models.User.prisma().create(types.UserCreateInput(id=id))

        return user
