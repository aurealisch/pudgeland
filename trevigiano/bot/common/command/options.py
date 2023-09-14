import dataclasses
import typing

import crescent
import hikari

Type = typing.Union[
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


@dataclasses.dataclass
class Option:
  type: Type
  name: str
  description: str


def option(
  type: Type,
  name: str,
  description: str,
) -> Option:
  return Option(
    type,
    name=name,
    description=description,
  )
