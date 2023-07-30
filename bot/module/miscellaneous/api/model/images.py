import msgspec


class Image(msgspec.Struct):
    id: str

    url: str

    width: int
    height: int
