"""."""


class YouCantDoThatError(Exception):
  """."""

  def __init__(self) -> None:
    """."""
    super().__init__('Так нельзя')


class NotEnoughBananaError(Exception):
  """."""

  def __init__(self) -> None:
    """."""
    super().__init__('Недостаточно бананов')


class NothingToCullError(Exception):
  """."""

  def __init__(self) -> None:
    """."""
    super().__init__('Нечего отбирать')


class NoAccessError(Exception):
  """."""

  def __init__(self) -> None:
    """."""
    super().__init__('Нет доступа')
