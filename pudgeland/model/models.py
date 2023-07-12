import attrs

from ..database import databases


@attrs.define
class Model:
    database: databases.Database = attrs.field(alias="db")
