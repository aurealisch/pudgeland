import typing

import attrs
import httpx
import msgspec
import yarl

from bot.module.miscellaneous.api.model import images as _image


@attrs.define
class ImageResource:
    url: yarl.URL

    def search(self) -> _image.Image:
        url = self.url

        with httpx.get(url) as response:
            content = response.content

            image = msgspec.json.decode(content, type=typing.Sequence[_image.Image])

        return image
