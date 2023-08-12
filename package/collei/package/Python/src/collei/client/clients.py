""""""

from __future__ import annotations

__all__: typing.Sequence[str] = (
    "Configuration",
    "URLs",
    "Image",
    "ImageResource",
    "Client",
)

import typing

import attrs
import msgspec
import requests
import yarl


@attrs.define
class Configuration:
    """"""

    url: yarl.URL


@attrs.define
class URLs:
    """"""

    configuration: Configuration

    def search(self) -> str:
        """"""
        return self.configuration.url / "images" / "search"


class Image(msgspec.Struct):
    """"""

    id: str

    url: str

    width: int
    height: int


@attrs.define
class ImageResource:
    """"""

    urls: URLs

    def search(self) -> typing.Sequence[Image]:
        """"""
        response = requests.get(self.urls.search())

        content = response.content

        buf = content

        image = msgspec.json.decode(buf, type=typing.Sequence[Image])

        return image


@attrs.define
class Client:
    """"""

    __url = yarl.URL("https://api.thedogapi.com/v1")

    __configuration = Configuration(__url)

    __urls = URLs(__configuration)

    __image_resource = ImageResource(__urls)

    @property
    def images(self) -> ImageResource:
        """"""
        return self.__image_resource
