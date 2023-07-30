import attrs
import requests

from bot.module.actions.api.enum.category import nsfw
from bot.module.actions.api.model import images


@attrs.define
class NsfwManager:
    def search(self, category: nsfw.NsfwCategory) -> images.Image:
        url = f"https://api.waifu.pics/nsfw/{category.value}"

        with requests.get(url) as response:
            image = images.Image(**response.json())

        return image
