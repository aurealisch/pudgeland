class YouCantDoThatError(Exception):
  def __init__(self) -> None:
    super().__init__('Так нельзя')


class NotEnoughBananaError(Exception):
  def __init__(self) -> None:
    super().__init__('Недостаточно бананов')
