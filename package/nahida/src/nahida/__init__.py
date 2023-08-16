from __future__ import annotations

__all__: typing.Sequence[str] = (
  'NSFWCategory',
  'SFWCategory',
  'Configuration',
  'URLs',
  'Image',
  'NSFWResource',
  'SFWResource',
  'Client',
)

import typing

import attrs
import requests
import yarl

NSFWCategory = typing.Literal[
  'waifu',
  'neko',
  'trap',
  'blowjob',
]
SFWCategory = typing.Literal[
  'waifu',
  'neko',
  'shinobu',
  'megumin',
  'bully',
  'cuddle',
  'cry',
  'hug',
  'awoo',
  'kiss',
  'lick',
  'pat',
  'smug',
  'bonk',
  'yeet',
  'blush',
  'smile',
  'wave',
  'highfive',
  'handhold',
  'nom',
  'bite',
  'glomp',
  'slap',
  'kill',
  'kick',
  'happy',
  'wink',
  'poke',
  'dance',
  'cringe',
]


@attrs.define
class Configuration:
  url: yarl.URL


@attrs.define
class URLs:
  configuration: Configuration

  def nsfw(self, category: NSFWCategory) -> str:
    return self.configuration.url / 'nsfw' / category

  def sfw(self, category: SFWCategory) -> str:
    return self.configuration.url / 'sfw' / category


@attrs.define
class Image:
  url: str


@attrs.define
class NSFWResource:
  urls: URLs

  def search(self, category: NSFWCategory) -> Image:
    url = self.urls.nsfw(category)

    response = requests.get(url) # pylint: disable=missing-timeout

    image = Image(**response.json())

    return image


@attrs.define
class SFWResource:
  urls: URLs

  def search(self, category: SFWCategory) -> Image:
    url = self.urls.sfw(category)

    response = requests.get(url) # pylint: disable=missing-timeout

    image = Image(**response.json())

    return image


@attrs.define
class Client:
  _url = yarl.URL('https://api.waifu.pics')

  _configuration = Configuration(_url)

  _urls = URLs(_configuration)

  _nsfw_resource = NSFWResource(_urls)
  _sfw_resource = SFWResource(_urls)

  @property
  def nsfw(self) -> NSFWResource:
    return self._nsfw_resource

  @property
  def sfw(self) -> SFWResource:
    return self._sfw_resource
