import attrs
import yarl

from bot.module.miscellaneous.api.resource import images


@attrs.define
class Client:
    url: yarl.URL = attrs.field()

    _image_resource = images.ImageResource(url)

    @property
    def image(self) -> images.ImageResource:
        return self._image_resource
