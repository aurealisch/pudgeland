import typing

import attrs


@attrs.define
class Environment:
  token: typing.Optional[str]
  url: typing.Optional[str]
  port: typing.Optional[int]
