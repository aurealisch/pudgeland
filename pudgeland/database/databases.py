import attrs
import replit

from .manager.user import UserManager


@attrs.define
class Database:
    database: replit.Database = attrs.field(alias="db")

    _user_manager = UserManager(database)

    @property
    def users(self) -> UserManager:
        return self._user_manager
