import datetime
import typing

Period = datetime.timedelta
Name = str
Plugins = typing.Iterable[str]
Token = str
Title = str
Description = str
Number = int
Identifier = str
Column = typing.Literal["berry", "fox", "coin", "netheriteScrap", "diamond"]
Value = int
Id = typing.Optional[str]
Berry = typing.Optional[int]
Fox = typing.Optional[int]
Coin = typing.Optional[int]
NetheriteScrap = typing.Optional[int]
Diamond = typing.Optional[int]
Start = typing.Union[float, int]
Stop = typing.Union[float, int]
Scraps = typing.Union[float, int]
Coins = typing.Union[float, int]
Diamonds = typing.Union[float, int]
Tame = typing.Union[float, int]
