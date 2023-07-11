import typing

import attrs
import replit


@attrs.define
class Database:
    database: replit.Database

    @property
    async def users(self) -> typing.Any:
        return self.database.get("users")
