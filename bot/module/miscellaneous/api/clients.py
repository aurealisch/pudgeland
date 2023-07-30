import attrs
import yarl

from bot.module.miscellaneous.api.manager import images


# Define an *attrs* class.
@attrs.define
class Client:
    # Identical to `attr.ib`, except keyword-only and with some arguments removed.
    url: yarl.URL = attrs.field()

    _image_manager = images.ImageManager(url)

    @property
    def image(self) -> images.ImageManager:
        return self._image_manager
