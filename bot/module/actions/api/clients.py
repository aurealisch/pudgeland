import attrs
import yarl

from bot.module.actions.api.configuration import configurations
from bot.module.actions.api.helper import urls
from bot.module.actions.api.resource import nsfw, sfw


@attrs.define
class Client:
    _url = yarl.URL("https://api.waifu.pics")

    _configuration = configurations.Configuration(_url)

    _urls = urls.Urls(_configuration)

    _nsfw_resource = nsfw.NsfwResource(_urls)
    _sfw_resource = sfw.SfwResource(_urls)

    @property
    def nsfw(self) -> nsfw.NsfwResource:
        return self._nsfw_resource

    @property
    def sfw(self) -> sfw.SfwResource:
        return self._sfw_resource


# MIT License
#
# Copyright (c) 2023 elaresai
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in all
# copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.
