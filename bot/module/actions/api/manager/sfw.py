import attrs
import httpx

from bot.module.actions.api.enum.category import sfw
from bot.module.actions.api.url import urls as _urls
from bot.module.actions.api.model import images


# Define an *attrs* class.
@attrs.define
class SfwManager:
    urls: _urls.Urls

    def search(self, category: sfw.SfwCategory) -> images.Image:
        url = self.urls.sfw(category)

        # Sends a `GET` request.
        with httpx.get(url) as response:
            image = images.Image(**response.json())

        return image
