import typing
import dataclasses


@dataclasses.dataclass
class Environment:
    host: typing.Any
    port: typing.Any
    user: typing.Any
    password: typing.Any
    database: typing.Any
