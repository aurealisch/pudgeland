import attrs

import prisma

from .manager import users


@attrs.define
class Database:
    prisma: prisma.Prisma

    _user_manager = users.UserManager(prisma)

    @property
    def users(self) -> users.UserManager:
        return self._user_manager
