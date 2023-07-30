import attrs
import yarl

from bot.module.actions.api.configuration import configurations
from bot.module.actions.api.manager import nsfw, sfw
from bot.module.actions.api.url import urls


@attrs.define
class Client:
    _url = yarl.URL("https://api.waifu.pics")

    _configuration = configurations.Configuration(_url)

    _urls = urls.Urls(_configuration)

    _nsfw_manager = nsfw.NsfwManager()
    _sfw_manager = sfw.SfwManager()

    @property
    def nsfw(self) -> nsfw.NsfwManager:
        return self._nsfw_manager

    @property
    def sfw(self) -> sfw.SfwManager:
        return self._sfw_manager
