import typing

import attrs
import msgspec
import requests

from bot.module.miscellaneous.api.model import images


@attrs.define
class ImageManager:
    url: str

    def search(self) -> images.Image:
        url = self.url

        with requests.get(url) as response:
            content = response.content

            image = msgspec.json.decode(content, type=typing.Sequence[images.Image])

        return image
