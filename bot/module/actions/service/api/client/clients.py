import typing

import attrs
import httpx

Category = typing.Literal["bite", "hug", "kiss", "lick", "poke"]


@attrs.define
class Configuration:
    url: str


@attrs.define
class Urls:
    configuration: Configuration

    def sfw(self, category: Category) -> str:
        return f"{self.configuration.url}/sfw/{category}"


@attrs.define
class Image:
    url: str


@attrs.define
class SfwResource:
    urls: Urls

    def search(self, category: Category) -> Image:
        url = self.urls.sfw(category)

        response = httpx.get(url)

        image = Image(**response.json())

        return image


@attrs.define
class Client:
    _url = "https://api.waifu.pics"

    _configuration = Configuration(_url)

    _urls = Urls(_configuration)

    _sfw_resource = SfwResource(_urls)

    @property
    def sfw(self) -> SfwResource:
        return self._sfw_resource


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
