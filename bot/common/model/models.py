import attrs
import hikari

from bot.common.configuration import configurations
from bot.common.database import databases
from bot.common.environment import environments


# Define an *attrs* class.
@attrs.define
class Model:
    configuration: configurations.Configuration
    database: databases.Database
    environment: environments.Environment

    # noinspection PyMethodMayBeStatic
    async def on_started_event(self, _: hikari.StartedEvent) -> None:
        # Connect to the Prisma query engine.
        await self.database.middleware.prisma.connect()

    # noinspection PyMethodMayBeStatic
    async def on_stopped_event(self, _: hikari.StoppedEvent) -> None:
        # Disconnect the Prisma query engine.
        await self.database.middleware.prisma.disconnect()


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
