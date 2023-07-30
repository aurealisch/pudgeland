import enum
import typing


@typing.final
class NsfwCategory(str, enum.Enum):
    WAIFU = "waifu"
    NEKO = "neko"
    TRAP = "trap"
    BLOWJOB = "blowjob"
