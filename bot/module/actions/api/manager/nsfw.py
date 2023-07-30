import attrs
import httpx

from bot.module.actions.api.enum.category import nsfw
from bot.module.actions.api.model import images
from bot.module.actions.api.url import urls as _urls


# Define an *attrs* class.
@attrs.define
class NsfwManager:
    urls: _urls.Urls

    def search(self, category: nsfw.NsfwCategory) -> images.Image:
        url = self.urls.nsfw(category)

        # Sends a `GET` request.
        with httpx.get(url) as response:
            image = images.Image(**response.json())

        return image
