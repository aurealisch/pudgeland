import attrs
import requests

from bot.module.actions.api.enum.category import sfw
from bot.module.actions.api.model import images


@attrs.define
class SfwManager:
    def search(self, category: sfw.SfwCategory) -> images.Image:
        url = f"https://api.waifu.pics/sfw/{category.value}"

        with requests.get(url) as response:
            image = images.Image(**response.json())

        return image
