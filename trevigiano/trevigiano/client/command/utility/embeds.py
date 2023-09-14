import typing

import hikari

Color = typing.Literal[
  'default',
  'error',
  'success',
]

colors = {
  'default': '#4f686d',
  'error': '#ff4b4b',
  'success': '#77b35a',
}


def embed(
  color: Color,
  title: typing.Optional[str] = None,
  description: typing.Optional[str] = None,
) -> hikari.Embed:
  color = hikari.Color.of(colors[color])

  embed = hikari.Embed(
    title=title,
    description=description,
    color=color,
  )

  return embed
