import dataclasses
import typing

import crescent
import hikari


@dataclasses.dataclass
class Option:
  type: typing.Union[
    type[str],
    type[bool],
    type[int],
    type[float],
    type['hikari.PartialChannel'],
    type['hikari.Role'],
    type['hikari.User'],
    type['crescent.Mentionable'],
    type['hikari.Attachment'],
  ]
  name: str
  description: str
