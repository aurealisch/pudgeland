import os

import crescent
import dotenv
import hikari
import miru
import msgspec

import prisma as _prisma
from .model import models

from ..core.configuration import configurations
from ..core.database import databases
from ..core.database.middleware import middlewares
from ..core.environment import environments

dotenv.load_dotenv()

with open("configuration.json") as stream:
    buffer = stream.read()

    configuration = msgspec.json.decode(buffer, type=configurations.Configuration)

prisma = _prisma.Prisma()

_prisma.register(prisma)

database = databases.Database(middlewares.Middleware(prisma))

token = os.environ.get("TOKEN")
url = os.environ.get("URL")

environment = environments.Environment(token, url=url)

bot = hikari.GatewayBot(environments.token, banner=configurations.gateway.bot.banner)

miru.install(bot)

model = models.Model(configuration, database=database, environment=environment)

bot.subscribe(hikari.StartedEvent, callback=models.on_started_event)
bot.subscribe(hikari.StoppedEvent, callback=models.on_stopped_event)

client = crescent.Client(bot, model=models)

for module in (
    "actions",
    "economics",
    "leaders",
    "miscellaneous",
    "reputation",
):
    client.plugins.load_folder(f"bot.modules.{module}.plugins")

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
