import msgspec


class UserStruct(msgspec.Struct):
    x: int
    y: int
