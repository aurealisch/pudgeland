import attrs
import yarl

from bot.module.actions.api.configuration import configurations
from bot.module.actions.api.enum.category import nsfw, sfw


@attrs.define
class Urls:
    configuration: configurations.Configuration

    def nsfw(self, category: nsfw.NsfwCategory) -> yarl.URL:
        return self.configuration.url / "nsfw" / category.value

    def sfw(self, category: sfw.SfwCategory) -> yarl.URL:
        return self.configuration.url / "sfw" / category.value
