import typing

import attrs


@attrs.define
class Environment:
  token: typing.Optional[str]
