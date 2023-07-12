import attrs
import hikari
import replit

from ..struct.user import UserStruct


@attrs.define
class UserManager:
    database: replit.Database = attrs.field(alias="db")

    def get(self, snowflake: hikari.Snowflakeish) -> UserStruct:
        pass
