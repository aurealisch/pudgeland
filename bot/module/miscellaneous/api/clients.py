import attrs
import yarl

from bot.module.miscellaneous.api.manager import images


@attrs.define
class Client:
    url: yarl.URL = attrs.field()

    _image_manager = images.ImageManager(url)

    @property
    def image(self) -> images.ImageManager:
        return self._image_manager
