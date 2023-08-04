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
import httpx
import msgspec


@attrs.define
class Configuration:
    """"""

    url: httpx.URL


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
        response = httpx.get(self.urls.search())

        content = response.content

        buf = content

        image = msgspec.json.decode(buf, type=typing.Sequence[Image])

        return image


@attrs.define
class Client:
    """"""

    __url = httpx.URL("https://api.thedogapi.com/v1")

    __configuration = Configuration(__url)

    __urls = URLs(__configuration)

    __image_resource = ImageResource(__urls)

    @property
    def images(self) -> ImageResource:
        """"""
        return self.__image_resource


# MIT License
#
# Copyright (c) 2023 elaresai
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in all
# copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.
