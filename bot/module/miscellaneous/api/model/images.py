import msgspec
import yarl


class Image(msgspec.Struct):
    id: str

    url: yarl.URL

    width: int
    height: int
