import typing

import attrs
import httpx
import msgspec
import yarl

from bot.module.miscellaneous.api.model import images


# Define an *attrs* class.
@attrs.define
class ImageManager:
    url: yarl.URL

    def search(self) -> images.Image:
        url = self.url

        # Sends a `GET` request.
        with httpx.get(url) as response:
            content = response.content

            image = msgspec.json.decode(content, type=typing.Sequence[images.Image])

        return image
