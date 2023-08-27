import typing

import crescent
import hikari
import miru

Mode = typing.Literal[
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
  mode: Mode,
  context: typing.Union[crescent.Context, miru.context.view.ViewContext],
  title: typing.Optional[str] = None,
  description: typing.Optional[str] = None,
  image: typing.Optional[hikari.files.Resourceish] = None,
) -> hikari.Embed:
  color = hikari.Color.of(colors[mode])

  contextual = context.user

  username = contextual.username
  avatar_url = contextual.avatar_url

  name = username
  icon = avatar_url

  _embed = (
    hikari.Embed(
      title=title,
      description=description,
      color=color,
    )
    .set_author(
      name=name,
      icon=icon,
    )
    .set_image(image)
  )

  return _embed
