import attrs

import prisma

from .manager import users


@attrs.define
class Database:
    prisma: prisma.Prisma

    _users_manager = users.UsersManager(prisma)

    @property
    def users(self) -> users.UsersManager:
        return self._users_manager
