""""""

from __future__ import annotations

__all__: typing.Sequence[str] = (
    "NSFWCategory",
    "SFWCategory",
    "Configuration",
    "URLs",
    "Image",
    "NSFWResource",
    "SFWResource",
    "Client",
)

import typing

import attrs
import requests
import yarl

NSFWCategory = typing.Literal["waifu", "neko", "trap", "blowjob"]
SFWCategory = typing.Literal[
    "waifu",
    "neko",
    "shinobu",
    "megumin",
    "bully",
    "cuddle",
    "cry",
    "hug",
    "awoo",
    "kiss",
    "lick",
    "pat",
    "smug",
    "bonk",
    "yeet",
    "blush",
    "smile",
    "wave",
    "highfive",
    "handhold",
    "nom",
    "bite",
    "glomp",
    "slap",
    "kill",
    "kick",
    "happy",
    "wink",
    "poke",
    "dance",
    "cringe",
]


@attrs.define
class Configuration:
    """"""

    url: yarl.URL


@attrs.define
class URLs:
    """"""

    configuration: Configuration

    def nsfw(self, category: NSFWCategory) -> str:
        """"""
        return self.configuration.url / "nsfw" / category

    def sfw(self, category: SFWCategory) -> str:
        """"""
        return self.configuration.url / "sfw" / category


@attrs.define
class Image:
    """"""

    url: str


@attrs.define
class NSFWResource:
    """"""

    urls: URLs

    def search(self, category: NSFWCategory) -> Image:
        """"""
        url = self.urls.nsfw(category)

        response = requests.get(url)

        image = Image(**response.json())

        return image


@attrs.define
class SFWResource:
    """"""

    urls: URLs

    def search(self, category: SFWCategory) -> Image:
        """"""
        url = self.urls.sfw(category)

        response = requests.get(url)

        image = Image(**response.json())

        return image


@attrs.define
class Client:
    """"""

    __url = yarl.URL("https://api.waifu.pics")

    __configuration = Configuration(__url)

    __urls = URLs(__configuration)

    __nsfw_resource = NSFWResource(__urls)
    __sfw_resource = SFWResource(__urls)

    @property
    def nsfw(self) -> NSFWResource:
        """"""
        return self.__nsfw_resource

    @property
    def sfw(self) -> SFWResource:
        """"""
        return self.__sfw_resource
