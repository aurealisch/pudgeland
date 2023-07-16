import attrs

import prisma


@attrs.define
class UserManager:
    prisma: prisma.Prisma

    async def find(
        self, *, id: str | prisma.types.StringFilter = ...
    ) -> prisma.models.User | None:
        user = await prisma.models.User.prisma().find_first(
            where=prisma.types.UserWhereInput(id=id)
        )

        if user is None:
            user = await prisma.models.User.prisma().create(
                prisma.types.UserCreateInput(id=id)
            )

        return user
