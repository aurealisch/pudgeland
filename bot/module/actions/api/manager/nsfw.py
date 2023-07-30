import attrs
import httpx

from bot.module.actions.api.enum.category import nsfw
from bot.module.actions.api.url import urls as _urls
from bot.module.actions.api.model import images


@attrs.define
class NsfwManager:
    urls: _urls.Urls

    def search(self, category: nsfw.NsfwCategory) -> images.Image:
        url = self.urls.nsfw(category)

        with httpx.get(url) as response:
            image = images.Image(**response.json())

        return image
