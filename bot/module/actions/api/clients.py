import attrs

from bot.module.actions.api.manager import nsfw, sfw


@attrs.define
class Client:
    _nsfw_manager = nsfw.NsfwManager()
    _sfw_manager = sfw.SfwManager()

    @property
    def nsfw(self) -> nsfw.NsfwManager:
        return self._nsfw_manager

    @property
    def sfw(self) -> sfw.SfwManager:
        return self._sfw_manager
