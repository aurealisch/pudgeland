import os

import crescent
import dotenv
import hikari
import miru
import msgspec

import prisma as _prisma

from ..core.configuration import configurations
from ..core.database import databases
from ..core.environment import environments
from .model import models

dotenv.load_dotenv()

with open("configuration.json") as stream:
    buffer = stream.read()

    configuration = msgspec.json.decode(buffer, type=configurations.Configuration)

prisma = _prisma.Prisma()

_prisma.register(prisma)

database = databases.Database(prisma)

token = os.environ.get("TOKEN")
url = os.environ.get("URL")

default = configuration.api.port.default

port = os.environ.get("PORT", default=default)

environment = environments.Environment(token, url=url, port=port)

banner = "bot"

bot = hikari.GatewayBot(environment.token, banner=banner)

miru.install(bot)

model = models.Model(configuration, database=database, environment=environment)

bot.subscribe(hikari.StartedEvent, callback=model.on_started_event)
bot.subscribe(hikari.StoppedEvent, callback=model.on_stopped_event)

client = crescent.Client(bot, model=model)

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
